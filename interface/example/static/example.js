
/*
Example of making an AJAX GET using jQuery and CoffeeScript
*/

(function() {
  var calculate, main, successful_addition;

  successful_addition = function(data) {
    /*
        Callback function for when a successful calculation was made.
        
        :param data: a jqXHR object containing the retrieved data.
    */    return $("#result").text(data.result);
  };

  calculate = function() {
    /*
        Makes the AJAX calculation request.
    */    return $.get("/add", {
      a: $("input[name='a']").val(),
      b: $("input[name='b']").val()
    }, successful_addition);
  };

  main = function() {
    /*
        Main script entry point.
    */    return $("a#calculate").bind("click", calculate);
  };

  $(function() {
    return main();
  });

}).call(this);
