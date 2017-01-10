function SimpleDM($, recognition, synthesis) {
  let $dm = this;

  this.status = {
    "clues": [],
    "context": [],
  };

  this.understand = function(text) {
    // understand text and update status
    // parse text? no parsing? shallow parsing!
    $dm.control(text);
  }

  this.generate = function() {
    // generate text based on status.
    //
    return
  }

  this.control = function(input) {
    if (typeof(input) == "string") {
      $.ajax({
          // The URL for the request
          url: "/game/i/update",

          // The data to send (will be converted to a query string)
          data: {
              clue: input
          },

          // Whether this is a POST or GET request
          type: "POST",

          // The type of data we expect back
          dataType : "json",
      })
        // Code to run if the request succeeds (is done);
        // The response is passed to the function
        .done(function(json) {
          // show the status of the model
          $("#status").html(JSON.stringify(json));
          $("#interface").html("");
          var reg = RegExp("lfw/(.+)/")

          json["context"].forEach(function(path){
             name = reg.exec(path)[1].replace("_", " ");
             $("#interface").append('<div class="item" data-item="'+path+'" ><img src="/img/'+path+'"/><div>'+name+'</div></div>');
             console.log(path);
          });

          json["guesswhos"].forEach(function(path){
             $("#interface .item[data-item='"+path+"']").addClass('candidate');
             console.log(path);
             console.log("#interface .item[data-item='"+path+"']");
          });

        })
        // Code to run if the request fails; the raw request and
        // status codes are passed to the function
        .fail(function( xhr, status, errorThrown ) {
          console.log( "Error: " + errorThrown );
          console.log( "Status: " + status );
          console.dir( xhr );
        })
        // Code to run regardless of success or failure;
        .always(function( xhr, status ) {
          console.log( "The request is complete!" );
        });
    }
  }
}
