var images;
var imagesLoaded = 0;


function loadLog()
{
  var aniIndex = 0;

  function preloadImageCallback(data)
  {
    imagesLoaded++;
    var progressBar = $('.loading-area div.progress-bar');
    var curProgress = 100.0 * imagesLoaded / images.length;
    progressBar.attr('style', 'width: ' + curProgress + '%;');
    progressBar.find('.sr-only').text(curProgress + '% complete');
    if (imagesLoaded == images.length)
    {
      setTimeout(beginAnimation, 750);
    }
  }

  function beginAnimation()
  {
    if (images.length > 0)
    {
      $('#animation-window .loading-area').fadeOut();
      setTimeout(animation, 50);
    }
  }

  function animation()
  {
    img = images[aniIndex];
    var imgSrc = 'https://s3.amazonaws.com/camuploadbobbotron/'+img['previewImage'];
    $('#animationTarget').attr('src', imgSrc);
    $('#animation-window p.timestamp').text(img['timestamp']);
    aniIndex = (aniIndex + 1) % images.length;
    var delay = aniIndex == 0 ? 2000 : 35;
    setTimeout(animation, delay);
  }
  function onDone(data)
  {
    var output = $('#photoOutput');
    function addImage(img)
    {
      var element = '<div><div class="coop-photo"><a href="https://s3.amazonaws.com/camuploadbobbotron/'+img['image']+'"><img class="coop-photo-img-preload" src="https://s3.amazonaws.com/camuploadbobbotron/'+img['previewImage']+'"/></a></div><p class="timestamp">'+img["timestamp"]+'</p></div>';

      output.append(element);
    }
    images = data;
    images.forEach(addImage);
    $('img.coop-photo-img-preload').on('load', preloadImageCallback);
    //setTimeout(beginAnimation, 2000);
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
