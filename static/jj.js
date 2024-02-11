setInterval(() => {
    var request=new XMLHttpRequest()
    request.open('GET',"weather")
    request.send()
    request.onload=() => {
        
        var jsonResponse=JSON.parse(request.response)
        var temp=document.getElementById("temperature")
        var hum=document.getElementById("humidity")
        var date=document.getElementById("date")
        var day=document.getElementById("day")
        var time=document.getElementById("time")
        var max_pred=document.getElementById("max_pred")
        var min_pred=document.getElementById("min_pred")

        temp.innerHTML=jsonResponse.temperature
        hum.innerHTML=jsonResponse.humidity
        date.innerHTML=jsonResponse.date
        day.innerHTML=jsonResponse.day
        time.innerHTML=jsonResponse.time
        max_pred.innerHTML=jsonResponse.max_pred
        min_pred.innerHTML=jsonResponse.min_pred

    }
},9000);


function loading(){
    document.getElementById("load").style.display="none";
}

const myTimeout = setTimeout(loading, 10000);

// WIP - Don't hate! I don't know javascript.
$('#toggle').click( function(){
    $(this).parent().toggleClass('width');
    $(this).children().toggleClass( 'fa-chevron-circle-left').toggleClass( 'fa-chevron-circle-right');
});


function send_to_django() {
    var location = document.getElementById('location').value;
    alert("wait...");
    document.getElementById("max_pred").style.display = 'inline-block';
    document.getElementById("min_pred").style.display = 'inline-block';
    document.getElementById("pre").style.display = 'inline-block';

    var url = '/weather/?location=' + encodeURIComponent(location);

    fetch(url, {
        method: 'GET',
        headers: {
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },
    })
    .then(response => response.text())
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
