$(document).ready(function(){
  let scheduled_function = false
  const users_div = $('#active_user')
  const endpoint = 'users'
  const delay_by_in_ms = 500

  let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters).done(response => {
            users_div.fadeTo('slow', 0).promise().then(() => {
            users_div.html(response['html_from_view'])
            users_div.fadeTo('slow', 1)
            })
        })
  }

  $("#user-input").on('keyup', function () {
    const request_params = {
      q: $(this).val()   
    }
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_params)

  });
});