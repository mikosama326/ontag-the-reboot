function onAppReady(){
    $('#go-to-gohunting').click(function(){
       $.ajax({
            url: 'http://192.168.43.249:5000/getSongs',
            type: 'GET',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success:function(rec) {
                songs = "<ul>"
                $.each(rec, function(id,song){
                    songs += "<li data-id="+id+" data-name="+song.songinfo['name']+" class='get-song'><a href='#song'         onclick='$.afui.clearHistory()' id='go-to-song'>" + song.songinfo['name'] + "</a></li>";
                });
                songs += "</ul>";
                $('#prey').text("");
                $('#prey').append(songs);
            }
        }); 
    });
}

document.addEventListener("deviceready", onAppReady, false);