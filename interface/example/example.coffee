###
Example of making an AJAX GET using jQuery and CoffeeScript
###

successful_addition = (data) ->
    ###
    Callback function for when a successful calculation was made.
    
    :param data: a jqXHR object containing the retrieved data.
    ###
    
    # Set the result span's text to the retrieved data
    $("#result").text data.result
    
calculate = ->
    ###
    Makes the AJAX calculation request.
    ###

    # Make the GET call
    $.get "/add", {
        # Get the values from the "a" and "b" text inputs and send them in the request.
        a: $("input[name='a']").val(),
        b: $("input[name='b']").val()
    }, successful_addition # callback function when the request was successful.
    
main = ->
    ###
    Main script entry point.
    ###
   
    # Bind the calculate  hyperlink to calculate the result
    $("a#calculate").bind "click", calculate

        
# Only run when document has loaded
$ ->
    main()
