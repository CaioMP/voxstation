from django.shortcuts import render, HttpResponse
from channel.models import *
from .process import *
from channel.process import ordena_pra_exibicao
from django.http import JsonResponse
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import Counter


def IndexView(request):
    contexto = {}

    mais_reproduzidos = checkVisib(audios=Audio.objects.order_by('-reproducoes'))
    melhor_avaliados = checkVisib(audios=Audio.objects.order_by('-numero_likes', 'numero_deslikes'))
    playlists = Playlist.objects.order_by('-reproducoes', '-numero_de_audios')
    for playlist in playlists:
        playlist.audios.set(checkVisib(audios=playlist.audios))
    playlists_pop = checkVisib(playlists=playlists)

    contexto['mais_reproduzidos'] = mais_reproduzidos
    contexto['melhor_avaliados'] = melhor_avaliados
    contexto['playlists_pop'] = playlists_pop

    if request.user.is_active:
        my_channels = Canal.objects.filter(proprietario=request.user).order_by('nome_canal')
        if my_channels.exists():
            contexto['my_channels'] = my_channels
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user).order_by('-ultima_atualizacao')
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user).order_by('nome_canal')
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user).order_by('-audio')
        for audio_notific in ntfs_audios.all():
            if audio_notific.audio.visibilidade == 'privado':
                audio_notific.delete()
        notifications = 0
        new_notific = 0

        if ntfs_audios.exists():
            for ntf in ntfs_audios.all():
                if not ntf.visualized:
                    new_notific += 1
                notifications += 1

        contexto['notifications'] = notifications
        contexto['new_notific'] = new_notific
        contexto['ntfs_audios'] = ntfs_audios
        fav = FeedLike.objects.filter(conta_feed=request.user).order_by('-data_do_feed')
        for audio_fav in fav.all():
            if audio_fav.Audio_feed.visibilidade == 'privado':
                audio_fav.delete()
        contexto['audios_favoritos'] = fav.all()

    contexto['logado'] = request.user.is_active

    if contexto['logado']:
        contexto['playlists'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canais_para_playlist'] = Canal.objects.filter(proprietario=request.user)
        contexto['channels'] = orderAudios(Canal.objects.filter(seguidor=request.user))

    return render(request, './home/index.html', contexto)


def search(request):
    contexto = {}

    if request.user.is_active:
        my_channels = Canal.objects.filter(proprietario=request.user).order_by('nome_canal')
        if my_channels.exists():
            contexto['my_channels'] = my_channels
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user).order_by('-ultima_atualizacao')
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user).order_by('nome_canal')
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user).order_by('-audio')
        for audio_notific in ntfs_audios.all():
            if audio_notific.audio.visibilidade == 'privado':
                audio_notific.delete()
        notifications = 0
        new_notific = 0

        if ntfs_audios.exists():
            for ntf in ntfs_audios.all():
                if not ntf.visualized:
                    new_notific += 1
                notifications += 1

        contexto['notifications'] = notifications
        contexto['new_notific'] = new_notific
        contexto['ntfs_audios'] = ntfs_audios
        fav = FeedLike.objects.filter(conta_feed=request.user).order_by('-data_do_feed')
        for audio_fav in fav.all():
            if audio_fav.Audio_feed.visibilidade == 'privado':
                audio_fav.delete()
        contexto['audios_favoritos'] = fav.all()

    if request.method == "POST":
        pesquisa = request.POST['pesquisa']
        if pesquisa.startswith("#"):
            for tag in Tag.objects.all(): # deletar a tag caso não existam mais áudios com ela
                ap = tag.get_aparicoes()
                if not ap:
                    tag.delete()

            tag_s = Tag.objects.filter(nome__istartswith=pesquisa[1:], nome__contains=pesquisa[1:])
            audios_tag_s = []
            if tag_s.exists():
                for audio in Audio.objects.all():
                    if audio.visibilidade != 'privado':
                        for tag in tag_s.all():
                            for tags_audio in audio.tag.all():
                                if tags_audio == tag:
                                    audios_tag_s.append(audio)

            contexto['tags_searched'] = tag_s
            contexto['audios_tag_s'] = audios_tag_s

        audios = Audio.objects.filter(titulo__contains=pesquisa)
        playlists = Playlist.objects.filter(nome__contains=pesquisa)

        contexto['pesquisa'] = pesquisa
        contexto['canais'] = Canal.objects.filter(nome_canal__contains=pesquisa)
        contexto['canais'] = checkExist(contexto['canais'])
        contexto['audios'] = checkExist(audios)
        contexto['audios'] = checkVisib(audios=contexto['audios'])
        contexto['playlists_show'] = checkExist(playlists)
        contexto['playlists_show'] = checkVisib(playlists=contexto['playlists_show'])

        if contexto['canais']:
            contexto['canais'] = contaSeg(contexto['canais'])

        if contexto['playlists_show']:
            contexto['playlists_show'] = ordena_pra_exibicao(contexto['playlists_show'])

        contexto['tot_result'], contexto['tot_playlists'], contexto['tot_audios'], contexto['tot_canais'] = contaResultados(contexto['canais'], contexto['audios'], contexto['playlists_show'])

    contexto['logado'] = request.user.is_active
    return render(request, './home/search.html', contexto)


def visualized(request):
    notifications = NotificAudio.objects.filter(user_notific=request.user)
    for notific in notifications:
        if not notific.visualized:
            notific.visualized = True
            notific.save()
    return HttpResponse("visualizado")


def report_audio(request, audio_id):
    audio = Audio.objects.get(pk=audio_id)

    fromaddr = "clientvxs@gmail.com"
    toaddr = "stationvox@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Denúncia " + audio.titulo

    body = "Áudio denunciado: http://127.0.0.1:8000/channel/audio/" + str(audio.pk) + \
           "\nCanal proprietário: " + audio.canal_proprietario.nome_canal + \
           "\nUsuário proprietário: " + audio.canal_proprietario.proprietario.email + \
           "\nDenunciante: " + request.user.email + \
           "\n\nMotivo: " + request.POST['motivo'] + \
           "\nDescrição: " + request.POST['denuncia']
    msg.attach(MIMEText(body, 'plain'))

    denuncia = AudioReport()
    denuncia.motivo = request.POST['motivo']
    denuncia.descricao = request.POST['denuncia']
    denuncia.usuario = request.user
    denuncia.audio = audio
    denuncia.canal = audio.canal_proprietario
    denuncia.save()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "80251997Client@")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    return HttpResponse("Email enviado")


def playordena(request, pesquisa):
    json = {}
    op = request.GET['op']

    if op == "recentes":
        playlists = Playlist.objects.filter(nome__contains=pesquisa).order_by('ultima_atualizacao').reverse()
    elif op == 'antigos':
        playlists = Playlist.objects.filter(nome__contains=pesquisa).order_by('ultima_atualizacao')
    elif op == "mais audios":
        playlists = Playlist.objects.filter(nome__contains=pesquisa).order_by('numero_de_audios').reverse()
    json['html'] = setOrdemPlaylistsSearch(playlists)

    return JsonResponse(json)


def audioordena(request, pesquisa):
    json = {}
    op = request.GET['op']
    audios = []
    hoje = datetime.today()
    if op == 'populares':
        audios = Audio.objects.filter(titulo__contains=pesquisa).order_by('reproducoes')
    elif op == 'melhor avaliados':
        audios = Audio.objects.filter(titulo__contains=pesquisa).order_by('numero_likes')
    elif op == "recentes":
        audios = Audio.objects.filter(titulo__contains=pesquisa).order_by('data_publicacao').reverse()
    elif op == "antigos":
        audios = Audio.objects.filter(titulo__contains=pesquisa).order_by('data_publicacao')

    json['html'] = setOrdemAudiosSearch(audios)
    return JsonResponse(json)


def ordenaCanais(request, pesquisa):
    json = {}
    op = request.GET['op']

    if op == 'mais seguidores':
        canais = Canal.objects.filter(nome_canal__contains=pesquisa).order_by('numero_seguidores').reverse()
    if op == 'mais recentes':
        canais = Canal.objects.filter(nome_canal__contains=pesquisa).order_by('data_criacao').reverse()
    if op == 'mais antigos':
        canais = Canal.objects.filter(nome_canal__contains=pesquisa).order_by('data_criacao')
    json['html'] = setOrdemCanais(canais)

    return JsonResponse(json)







