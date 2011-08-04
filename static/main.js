$(document).ready(function() { 
	//$('#tweets div.tr:even').css('background-color','#dddddd');
	//$('#celebs div.tr:odd').css('color', '#666666');
	$('.button').live('click', function() {
		$('#loader').addClass('show').removeClass('hide');
		$('.button').hide();
		$('#not').hide();
	}); 
});

