let get_input_text = function() {
    let event_name = $("input#event_name").val()
    let event_description = $("textarea#event_description").val()
    let event_date = $("input#event_date").val()
    let event_time = $("input#event_time").val()
    let event_visibility = $("select#event_visibility").val()
    return {'name': event_name,
            'plain_text_no_images_description': event_description,
            'local_date': event_date,
            'local_time': event_time,
            'visibility': event_visibility}
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
