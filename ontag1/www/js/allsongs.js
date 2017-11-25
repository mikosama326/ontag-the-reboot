function loadSongs(){
    information = JSON.parse(window.localStorage.getItem('information'));
    
    delete information.user;
    delete information.playlists;
    
    songs = "<ul>"
    
    $.each(information, function(id,song){
                    
        songs += "<li data-id="+id+" data-page='songs' class='play-song'><a href='#song'         onclick='$.afui.clearHistory()' id='go-to-song'>" + song.songinfo['name'] + "</a></li>";
        
    });
    
    songs += "</ul>";
    
    $('#songs-local').html(songs);
    
}

document.addEventListener("deviceready", loadSongs, false);;



