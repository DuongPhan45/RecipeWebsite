// don't execute any JS until after the DOM is loaded

$(document).ready(function () {

    // call the hide function
    $('ol>li').hide();
   
    $('ul>li').hide();
    // $('ul>.new').show();

    $('#ingredientList').hide();

    // reveal list item
    $('#showIngredient').click(function () {
        $('ul > li:hidden:first').show();
    });

    $('#showStep').click(function () {
        $('ol > li:hidden:first').show();
    });

    // listen for events at the button
    $('#btn').click(function () {
        // if the input text is not null, append it to the list
        if ($('#text').val() != '') {
            $('#ingredient').append('<li>' + $('#text').val() + '</li>').hide();
            // clear inputted text from the text field
            $('#text').val('');
        }
        // prevent the button to reload the page after being clicked
        return false;
    });

    $('#btn1').click(function () {
        // if the input text is not null, append it to the list
        if ($('#text1').val() != '') {
            $('#step').append('<li>' + $('#text1').val() + '</li>');
            // clear inputted text from the text field
            $('#text1').val('');
        }
        // prevent the button to reload the page after being clicked
        return false;
    });

});

