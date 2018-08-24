let get_input_text = function() {
    let text_input = $("input#userTextInput").val()
    //let variable = $("input#idofthing").val()
    return {'text_input': text_input} //this thing behaves like a dict
};
let send_text_json = function(text_input) {
    $.ajax({
        url: '/submit',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            display_solutions(data);
        },
        data: JSON.stringify(text_input)
    });
};
let display_solutions = function(predictions) {
    $("span#prediction").html(predictions.prediction)
};
let predict = function() {
        let text_input = get_input_text();
        send_text_json(text_input);
    }
