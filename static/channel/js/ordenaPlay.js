$('document').ready( function(){
	$('.opPlay').on('click',function(){
		var this_ = $(this);
		var datas = {'opcao':this_.attr('val')};
		console.log(datas);
		console.log($('#caminhoPlay').attr('identifier'));
		$.ajax({
			url:$('#caminhoPlay').attr('identifier'),
			type:'GET',
			beforeSend:function(){
				
			},
			dataType:'json',
			async:true,
			data:datas,
			success:function(json){
				$("#container_plays").html(json.html)
			},
			error:function(){
				
			}
		});
	});
});