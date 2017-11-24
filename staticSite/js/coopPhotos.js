function loadLog()
{
  function onDone(data)
  {
    var output = $('#photoOutput');
    function addImage(img)
    {
      var element = '<div><div class="coop-photo"><a href="https://s3.amazonaws.com/camuploadbobbotron/'+img['image']+'"><img class="coop-photo-img" src="https://s3.amazonaws.com/camuploadbobbotron/'+img['previewImage']+'"/></a></div><p class="timestamp">'+img["timestamp"]+'</p></div>';

      // console.log("Appending " + element );
      // todo animation on image load?
      output.append(element);
    }
    data.reverse().forEach(addImage);
    $('.loading-area').fadeOut();
  }
  $.getJSON(
  "https://s3.amazonaws.com/camuploadbobbotron/coop1/log.json",
  {})
  .done(onDone)
  .fail(function() {
    console.log( "error" );
  })
  .always(function() {
    console.log( "complete" );
  });
}

$(loadLog);

/*
var flickerAPI = "http://api.flickr.com/services/feeds/photos_public.gne?jsoncallback=?";
$.getJSON( flickerAPI, {
  tags: "mount rainier",
  tagmode: "any",
  format: "json"
})
  .done(function( data ) {
    $.each( data.items, function( i, item ) {
      $( "<img>" ).attr( "src", item.media.m ).appendTo( "#images" );
      if ( i === 3 ) {
        return false;
      }
    });
  });
})();
*/
