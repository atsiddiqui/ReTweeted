
function is_following(following_list, o_screen_name) {
	var sn = "'"+o_screen_name+"'";
	var following;
	for(var f=0; f<following_list.length; f++)  {
		var fl = jQuery.trim(following_list[f]);
		if(sn == fl) {
			following = true;
			return following
		}
	}
	return following
	
}
function lightbox(screen_name, o_screen_name, url){
	following_list = $("#following_list").val();
	following_list = following_list.replace('[', '');
	following_list = following_list.replace(']', '');
	following_list = following_list.split(',');
	
	if($('#lightbox').size() == 0){
		var theLightbox = $('<div id="lightbox"/>');
		var theShadow = $('<div id="lightbox-shadow"/>');
		$(theShadow).click(function(e){
			closeLightbox();
		});
		$('body').append(theShadow);
		$('body').append(theLightbox);
	}
	$('#lightbox').empty();
	
	if(url != null){
		//$('#lightbox').append('<span class="loading">Loading...</span>');
		$('#lightbox').append('<span class="top_area">Retweeted By: </span>');
		$('#lightbox').append('<div id="search_area" align="right"><span><img class="close-icon" src="/media/images/close-icon.gif" /></span></div>');
		$.getJSON(url, function(response) 
		{
		    for(i = 0; i < response.length; i++)
		    {
			
			if(response[i].screen_name == screen_name) {
		        $('#lightbox').append('<div class="friends_area"><img src="' +response[i].profile_image_url_https+ '"height="50" style="float:left;"/><a style="text-decoration:none" href="http://twitter.com/'+response[i].screen_name+'" target="blank"><label class="name" style="float: left;">'+response[i].screen_name+'</label></a><a style="text-decoration:none" href="#"><span class="follow-box-self">You!</span></a></div>');
			} else if(is_following(following_list, response[i].screen_name) == true ) {
				$('#lightbox').append('<div class="friends_area"><img src="' +response[i].profile_image_url_https+ '"height="50" style="float:left;"/><a style="text-decoration:none" href="http://twitter.com/'+response[i].screen_name+'" target="blank"><label class="name" style="float: left;">'+response[i].screen_name+'</label></a><a style="text-decoration:none" href="#"><span id="u_'+response[i].screen_name+'" class="follow-box-unfollow">Unfollow</span><span id="f_'+response[i].screen_name+'" class="follow-box hide">Follow</span></a><img src="/media/images/loader.gif" class="hide" id="unfollow_load" /></div>');
			}
			else {
			$('#lightbox').append('<div class="friends_area"><img src="' +response[i].profile_image_url_https+ '"height="50" style="float:left;"/><a style="text-decoration:none" href="http://twitter.com/'+response[i].screen_name+'" target="blank"><label class="name" style="float: left;">'+response[i].screen_name+'</label></a><a style="text-decoration:none" href="#"><span id="f_'+response[i].screen_name+'" class="follow-box">Follow</span><span id="u_'+response[i].screen_name+'" class="follow-box-unfollow hide">Unfollow</span></a><img src="/media/images/loader.gif" class="hide" id="follow_load" /></div>');
			}
			
		    }
		});
	}
	$('#lightbox').css('top', $(window).scrollTop() + 100 + 'px');
	$('#lightbox').show();
	$('#lightbox-shadow').show();
}
function closeLightbox(){
	$('#lightbox').hide();
	$('#lightbox-shadow').hide();
	$('#lightbox').empty();
}

$(document).ready(function() { 
	//$('#tweets div.tr:even').css('background-color','#dddddd');
	//$('#celebs div.tr:odd').css('color', '#666666');
	$('#lightbox').elastic();
	$('.button').live('click', function() {
		$('#loader').addClass('show').removeClass('hide');
		$('#message').addClass('show').removeClass('hide');
		$('.button').hide();
		$('#not').hide();
		
	}); 
	$('.close-icon').live('click', function() {
		$('#lightbox').hide();
		$('#lightbox-shadow').hide();
		$('#lightbox').empty();
	});

	$('span[id^="u_"]').live('click', function() {
		id = this.id
		number_array = id.split("_");
		screen_name = number_array[1];
		$("#"+id).addClass("hide").removeClass("show");
		$("#unfollow_load").addClass('show').removeClass('hide');
		var url = "/unfollow/"
		$.ajax({
			type:'POST',
			url:url,
			data:{"screen_name":screen_name},
			success:function(data) {
				$("#f_"+screen_name).addClass("show").removeClass("hide");	
				$("#unfollow_load").addClass('hide').removeClass('show');	
			},
			dataType:"json"
		});
		return false;
	});

        $('span[id^="f_"]').live('click', function() {
		id = this.id
		number_array = id.split("_");
		screen_name = number_array[1];
		$("#"+id).addClass("hide").removeClass("show");
		$("#unfollow_load").addClass('show').removeClass('hide');
		var url = "/follow/"
		$.ajax({
			type:'POST',
			url:url,
			data:{"screen_name":screen_name},
			success:function(data) {
				$("#u_"+screen_name).addClass("show").removeClass("hide");
				$("#unfollow_load").addClass('hide').removeClass('show');
			},
			dataType:"json"
		});
		return false;
	});
});

