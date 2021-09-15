$(document).ready(function() {

  $('menu_request').on('click',function() {
    var itemid = $(this).attr('buttonid')
    req = $.ajax({
      url : '/update',
      type : '/post',
      data : {itemid : itemid}

    });

    req.done(function(data) {

    });

  });

});