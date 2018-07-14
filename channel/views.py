from django.shortcuts import render, HttpResponse,redirect, reverse
from .forms import AudioForm, TagForm,SearchChannelAudioForm
from .models import Audio,Tag
from account.models import Canal
from .process import *
from account.models import MyUser

def myuploads(request):
    audio = Audio()
    channels = Canal.objects.filter(proprietario=request.user)

    if request.method == "POST":
        tagform = TagForm(request.POST)
        form = AudioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and tagform.is_valid():
            form.save(commit=False)
            audio.canal_proprietario = form.cleaned_data["canal_proprietario"]
            audio.titulo = form.cleaned_data['titulo']
            audio.audio = form.cleaned_data['audio']
            audio.descricao = form.cleaned_data['descricao']
            audio.capa = form.cleaned_data['capa']
            audio.likes = 1
            audio.deslikes = 1
            audio.audiencia = 0
            audio.reproducoes = 0
            audio.proprietario = request.user
            audio.save()
            tagtext = tagform.cleaned_data['text']
            taglist = tagprocess(tagtext)
            for tagitem in taglist:
                query = Tag.objects.filter(nome=tagitem)
                if query.exists():
                    audio.tag.set(query)
                    audio.save()
                else:
                    query = Tag.objects.create(nome=tagitem)
                    query.save()
                    query = Tag.objects.filter(nome=tagitem)
                    audio.tag.set(query)
                    audio.save()

            return redirect('/')
        else:
            erro = True
            return render(request, "./channel/myuploads.html", {'form': form, 'channels': channels, 'logado': request.user.is_active,
                                                                "tagform": tagform, "erro": erro})
    tagform = TagForm()
    form = AudioForm(instance=request.user)
    return render(request, "./channel/myuploads.html", {'form': form, 'channels': channels,
                                                        "tagform": tagform, 'logado': request.user.is_active})


def channel(request, nome):
    contexto={}
    contexto['chan'] = getaudios(Canal.objects.get(nome_canal=nome))
    contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
    contexto['logado'] = request.user.is_active
    if request.user == contexto['chan'].proprietario:
        contexto['direito_edicao']=True
    else:
        contexto['direito_edicao']=False
    return render(request, './channel/channel.html', contexto)


def playlist(request,nome):
    contexto = {}
    contexto['logado'] = request.user.is_active
    contexto['chan'] = Canal.objects.get(nome_canal=nome)
    if request.user == contexto['chan'].proprietario:
        contexto['direito_edicao'] = True
    else:
        contexto['direito_edicao'] = False
    contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
    return render(request, './channel/playlists.html', contexto)


def about(request, nome):
    contexto = {}
    contexto['logado'] = request.user.is_active
    contexto['chan'] = Canal.objects.get(nome_canal=nome)
    contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
    audios = Audio.objects.filter(canal_proprietario=contexto['chan'])
    contexto['likes'] = get_status_channel(audios, 'likes')
    contexto['deslikes'] = get_status_channel(audios, 'deslikes')
    contexto['reproducoes_tot'] = get_status_channel(audios)
    contexto['tags_mais_usadas'] = get_tags(audios)
    if request.user == contexto['chan'].proprietario:
        contexto['direito_edicao'] = True
    else:
        contexto['direito_edicao'] = False
    return render(request, './channel/about.html', contexto)


def uploads(request, nome):
    contexto= {}
    contexto['logado'] = request.user.is_active
    contexto['chan'] = Canal.objects.get(nome_canal=nome)
    contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
    if request.user == contexto['chan'].proprietario:
        contexto['direito_edicao'] = True
    else:
        contexto['direito_edicao'] = False

    if request.method == 'POST':
        search_form = SearchChannelAudioForm(request.POST)

        if search_form.is_valid():
            search = search_form.cleaned_data['text']
            audios = searchclear(search, contexto['chan'])
            contexto['audios'] = audios
            contexto['form_aud'] = SearchChannelAudioForm()
            return render(request, './channel/uploads.html', contexto)
        else:
            contexto['erro'] = True
            contexto['form_aud'] = SearchChannelAudioForm()
            return render(request, './channel/uploads.html', contexto)
    else:
        audios = Audio.objects.filter(canal_proprietario=contexto['chan']).order_by('data_publicacao').reverse()
        contexto['audios'] = audios
        contexto['form_aud'] = SearchChannelAudioForm()
        return render(request, './channel/uploads.html', contexto)


def partner(request, nome):
    return render(request, './channel/similar.html')


def playlist_all(request):
    return render(request, './channel/playlist_all.html')
