
$(document).on('click','#createEvent',function(event){
   var data = validate_data();
   if (data){
      create_event(data)
   } else{
      event.preventDefault();
   }

});

function create_event(data){

   $.ajax({
      url: "/api/v1/events/",
      type : "POST",
      data: JSON.stringify(data),
      success: function( result ) {
         var url = window.location.href.split('/');
         url.splice(3,1);
         alert('Log Salvo com Sucesso!');
         window.location.href = url.join('/');
      }
   });
}

function validate_data(){
    var start_date = $( "input[name='start_date']" ).val();
    var end_date = $( "input[name='end_date']" ).val();
    var category_id = $("#select_category").val();
    var note = $( "input[name='note']" ).val();
    if (start_date === ""){
        alert('this field is required');
        return false
    }
    return {
        start_date: start_date,
        end_date: end_date,
        note: note,
        category_id: category_id
      }
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    contentType: "application/json",
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
    }
});
