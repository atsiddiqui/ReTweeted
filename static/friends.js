function urlize(x) {
	list = x.match( /\b(http:\/\/|www\.|http:\/\/www\.)[^ ]{2,100}\b/g );
	if (list) {
		    x = x.replace( list, "<a style='color:#DD4B39;'target='_blank' href='" + list + "'>"+ list + "</a>" );
	}
	return x;
};


function lightbox(screen_name, url){
	
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
		$('#lightbox').append('<span class="top_area">'+screen_name+' recent retweets: </span>');
		$('#lightbox').append('<div id="friends_bar" align="right"><span><img class="close-icon" src="/media/images/close-icon.gif" /></span></div>');
		$.getJSON(url, function(response) 
		{
		    if(response.length > 0) {
			    for(i = 0; i < response.length; i++)
			    {
				var tweet_text = urlize(response[i].retweeted_status.text);
				$('#lightbox').append('<div class="friends_message">' +tweet_text+ '</div>');
							
			    }
		    } else {
				$('#lightbox').append('<div class="friends_message">Oops! no retweet found.</div>');
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
	
	$('.close-icon').live('click', function() {
		$('#lightbox').hide();
		$('#lightbox-shadow').hide();
		$('#lightbox').empty();
	});

	$('#tweetthis').live('click', function() {
		$("#loader-img").addClass("show").removeClass("hide");
		var url = "/post/"
		$.ajax({
			type:'POST',
			url:url,
			data:{"message":$('#hidden-val').val()},
			success:function(data) {
				$("#loader-img").addClass("hide").removeClass("show");	
			},
			dataType:"json"
		});
		return false;
	});

});

