/* Custom jQuery scripts */
jQuery(document).ready(function($) {

	"use strict";

          /* banner slider */
	      $('#banner-slide').bjqs({
            animtype      : 'slide',
            height        : 417,
            width         : 705,
            responsive    : true,
            randomstart   : true
          });
		  
		  
		  
          /* Tooltip */
		  $(function () {
			
			'use strict';
			  
           $('[data-toggle="tooltip"]').tooltip()
        })		  
		  
		  
		  
          /* Back to Top link */
	       $('.back-top').click(function(){
			   
			'use strict';
			   
		   $('html, body').animate({scrollTop:0}, 'fast');
		   return false;
	      });
	

	
	
});// - document ready