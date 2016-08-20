$(function(){
	$(".backclass").click(function(){
		var ua = navigator.userAgent.toLowerCase();
		if(/iphone|ipad|ipod/.test(ua)){
			window.location.href="xuebaBack";
		}else if (/android/.test(ua)){
			window.localMethod.back();
		}else{
			window.history.back();
		}
	});
	$(".inclass,footer a").on('touchstart touchend',function(){
		$(this).toggleClass("active-p");
	});
	$(".inclass").on('click', function(){
		var ua = navigator.userAgent.toLowerCase();
		if (/iphone|ipad|ipod/.test(ua)) {
			    // alert("iphone");
		} else if (/android/.test(ua)) {
			window.localMethod.startRTS($(this).parent().find(".title").text(),sessionId);
		}
	});
	$(".abclass").click(function(){
		alert("该功能正在开发！");
	});
});