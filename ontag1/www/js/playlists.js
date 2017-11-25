function loadPlaylists(){
    playlists = JSON.parse(window.localStorage.getItem("playlists"));
    mapping = JSON.parse(window.localStorage.getItem("mapping"));
    pl = "<ul>";
    $.each(playlists,function(playlist){
       pl += "<li data-playlist="+playlist+" class='playlist'><a href='#playlist' onclick='$.afui.clearHistory()' id='go-to-songs'>"+playlist+"</a></li>"; 
    });
    pl += "</ul>";
    $('#pl').append(pl);
}

document.addEventListener("deviceready", loadPlaylists, false);