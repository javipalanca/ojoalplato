(function( $ ) {
    "use strict";
    
    $(window).load(function() {
	    
	    //These functions are affected by fonts loading
	    
	});
    
	$( document ).ready(function() {
		
		$(".hentry").fitVids();
		
		$(".hentry a[href$='jpg'],.hentry a[href$='jpeg'],.hentry a[href$='png'],.hentry a[href$='gif']").colorbox({
			rel:'gallery',
			maxWidth: '90%',
			maxHeight: '90%'
		});
		
		$( ".site-navigation .navbar-toggle" ).click(function() {
			$(this).toggleClass("collapsed");
			$("body").toggleClass("mobile-nav-open");
		});
		
		$( ".site-navigation .menu li" ).hover(function() {
			$(this).addClass("hover");
		}, function() {
			$(this).removeClass("hover");
		});
		
		$( ".site-navigation .menu li.menu-item-has-children>a" ).click(function() {
			var windowWidth = Math.max( $(window).width(), window.innerWidth);
			var parentListItem = $(this).parent("li");
			if (windowWidth < 768) {
				if (parentListItem.hasClass("opened")) {
					//parentListItem.removeClass("opened");
				} else {
					parentListItem.addClass("opened");
					return false;
				}
				
			}
		});

	});
	
}(jQuery));