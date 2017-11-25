function onAppReady(){
    information = JSON.parse(window.localStorage.getItem('information'));
    pl = JSON.parse(window.localStorage.getItem("playlists"));
    mapping = JSON.parse(window.localStorage.getItem("mapping"));
    user = information.user;
    playlists = information.playlists;
    delete information.user;
    delete information.playlists;
    
    //$('source').attr("src","sounds/boot-sound.wav");
    //$('source').attr("type","audio/wav");
        
    $("#go-to-songs").click(function(){
       information = JSON.parse(window.localStorage.getItem('information'));
    
        songs = "<ul>"

        $.each(information, function(id,song){

            songs += "<li data-id="+id+" data-page='songs' class='play-song'><a href='#song'         onclick='$.afui.clearHistory()' id='go-to-song'>" + song.songinfo['name'] + "</a></li>";

        });

        songs += "</ul>";

        $('#songs-local').text("");
        $('#songs-local').html(songs); 
    });
    
    
    $(document).on('click','.play-song',function(){
        var data = {
            user: user,
            playlists: playlists
        };
        data[$(this).data("id")] = information[$(this).data("id")];
        $.ajax({
            url: 'http://192.168.43.249:5000/recommend',
            type: 'GET',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            success:function(rec) {
                delete rec.user;
                delete rec.playlists;
                console.log(rec);
                songs = "<ul>"
                $.each(rec, function(id,song){
                    songs += "<li data-id="+id+" data-name="+song.songinfo['name']+" class='get-song'><a href='#song'         onclick='$.afui.clearHistory()' id='go-to-song'>" + song.songinfo['name'] + "</a></li>";
                });
                songs += "</ul>";
                $('.recommendations').text("");
                $('.recommendations').append(songs);
            }
        });
        $('#songinfo').text($(this).text());
        //$('source').attr("src","sounds/"+$(this).text()+".wav");
        window.requestFileSystem(LocalFileSystem.PERSISTENT, 0, function(fs){
            fs.root.getDirectory('songs',{create: false}, function(dirEntry){
                $('source').attr("src",dirEntry.toURL()+$('#songinfo').text()+".wav");
                $('source').attr("type","audio/wav");
                $('audio').load();
                $('audio').trigger("play");
            });
        });
        
        
        
        
        $("h1").text(information[$(this).data('id')].songinfo['name']);
        var list = "<ul>";
        $.each(information[$(this).data('id')].playlists,function(key,present){
           if(present)
                list += "<li data-playlist="+mapping[key]+" class='playlist'><a href='#playlist' onclick='$.afui.clearHistory()' id='go-to-playlist'>"+mapping[key]+"</a></li>";
        });
        list += "</ul>\
                <button id='edit-playlists' data-id='"+$(this).data('id')+"'>Edit</button>";
        $("#song-playlists").text("");
        $("#song-playlists").append(list);
    });
    
    
    $(document).on('click','.playlist',function(){
        $("h1").text($(this).data("playlist"));
        songs = "<ul>";
        $.each(pl[$(this).data("playlist")],function(key,id){
           songs += "<li data-id="+id+" data-page='playlist' class='play-song'><a href='#song'  onclick='$.afui.clearHistory()' id='go-to-song'>" + information[id].songinfo['name'] + "</a></li>"; 
        });
        songs += "</ul>";
        
        $("#playlist-local").text("");
        $("#playlist-local").append(songs);
        
    });
    
    
    $(document).on('click','#edit-playlists',function(){
        var yes = "<ul id='yes-list'>";
        var no = "<ul id='no-list'>";
        $.each(information[$(this).data('id')].playlists,function(key,present){
           if(present)
                yes += "<li data-playlist="+key+" class='yes'><i class='icon remove'></i>"+mapping[key]+"</li>";
            else
                no += "<li data-playlist="+key+" class='no'><i class='icon add'></i>"+mapping[key]+"</li>";
        });
        yes += "</ul>";
        no += "</ul>";
        var button = "<button id='confirm' data-id='"+$(this).data('id')+"'>Confirm</button>\
                        <button id='cancel' data-id='"+$(this).data('id')+"'>Cancel</button>";
        $("#song-playlists").text("");
        $("#song-playlists").append(yes+"<hr>"+no+"<hr>"+button);
    });
    
    $(document).on('click','#cancel',function(){
        var list = "<ul>";
        $.each(information[$(this).data('id')].playlists,function(key,present){
           if(present)
                list += "<li data-playlist="+mapping[key]+" class='playlist'><a href='#playlist' onclick='$.afui.clearHistory()' id='go-to-playlist'>"+mapping[key]+"</a></li>";
        });
        list += "</ul>\
                <button id='edit-playlists' data-id='"+$(this).data('id')+"'>Edit</button>";
        $("#song-playlists").text("");
        $("#song-playlists").append(list);
    });
    
    $(document).on('click','.no',function(){
        $('#yes-list').append("<li data-playlist="+$(this).data('playlist')+" class='yes'><i class='icon remove'></i>"+mapping[$(this).data('playlist')]+"</li>");   
        $(this).remove();
    });
    
    $(document).on('click','.yes',function(){
        $('#no-list').append("<li data-playlist="+$(this).data('playlist')+" class='no'><i class='icon add'></i>"+mapping[$(this).data('playlist')]+"</li>");   
        $(this).remove();
    });
    
    $(document).on('click','#confirm',function(){
        var id = $(this).data('id');
        var p = [];
        for(var i=0; i<playlists; i++)
            p[i] = 0;
        $('#yes-list').children('li').each(function(){
           p[$(this).data('playlist')] = 1;
        });
        
        info = JSON.parse(window.localStorage.getItem('information'));
        info[id]['playlists'] = p;
        information[id]['playlists'] = p;
        window.localStorage.setItem("information",JSON.stringify(info));
        var count = parseInt(window.localStorage.getItem('count'));
        count += 1;
        if(count==2)
            {
            $.ajax({
                url: 'http://192.168.43.249:5000/fit',
                type: 'GET',
                dataType: 'text',
                contentType: 'application/json; charset=utf-8',
                data: window.localStorage.getItem('information'),
                success:function(res) {
                }
            });
            count=0;
            }
        window.localStorage.setItem('count',count);
        var list = "<ul>";
        $.each(information[id].playlists,function(key,present){
           if(present)
               {
                list += "<li data-playlist="+mapping[key]+" class='playlist'><a href='#playlist' onclick='$.afui.clearHistory()' id='go-to-playlist'>"+mapping[key]+"</a></li>";
                if($.inArray(id,pl[mapping[key]])==-1)
                    pl[mapping[key]].push(id);
               }
            else
                {
                if($.inArray(id,pl[mapping[key]])>-1)
                   pl[mapping[key]].splice($.inArray(id,pl[mapping[key]]),1);
                }
        });
        window.localStorage.setItem('playlists',pl);
        list += "</ul>\
                <button id='edit-playlists' data-id='"+id+"'>Edit</button>";
        $("#song-playlists").text("");
        $("#song-playlists").append(list);
    });
    
    
    $(document).on('click','.get-song',function(){
        var songname = $(this).data('name');
        var id = $(this).data('id');
        window.requestFileSystem(LocalFileSystem.PERSISTENT, 0, function (fs) {
 
            fs.root.getDirectory('songs',{create: false}, function(dirEntry){
                var fileTransfer = new FileTransfer();
                var uri = encodeURI("http://192.168.43.249:5000/fetch?song="+songname);
                //"use strict" ;
                var path = dirEntry.toURL();
                fileURL = path+songname+".wav";
                var directoryEntry = path;
                fileTransfer.download(
                    uri,
                    fileURL,
                    function(entry) {
                        var data = {
                            user: user,
                            playlists: playlists
                        };
                        songinfo = {
                            name: songname
                        };
                        data[id] = {
                            songinfo: songinfo
                        };
                        $.ajax({
                            url: 'http://192.168.43.249:5000/predict',
                            type: 'GET',
                            dataType: 'json',
                            contentType: 'application/json; charset=utf-8',
                            data: JSON.stringify(data),
                            success:function(pred) {
                                song = "<li data-id="+id+" data-page='songs' class='play-song'><a href='#song'  onclick='$.afui.clearHistory()' id='go-to-song'>" + songname + "</a></li>";
                                $('#songs-local').append(song);
                                $('source').attr("src",entry.toURL());
                                $('source').attr("type","audio/wav");
                                $('audio').load();
                                $('audio').trigger("play");
                                delete pred.user;
                                delete pred.playlists;
                                info = JSON.parse(window.localStorage.getItem('information'));
                                info[id] = pred[id];
                                information[id] = pred[id];
                                window.localStorage.setItem("information",JSON.stringify(info));
                                $.each(information[id].playlists,function(key,present){
                                    if(present==1)
                                        pl[mapping[key]].push(id.toString());
                                });
                                window.localStorage.setItem("playlists",pl);
                                var count = parseInt(window.localStorage.getItem('count'));
                                count += 1;
                                if(count==2)
                                    {
                                    $.ajax({
                                        url: 'http://192.168.43.249:5000/fit',
                                        type: 'GET',
                                        dataType: 'text',
                                        contentType: 'application/json; charset=utf-8',
                                        data: window.localStorage.getItem('information'),
                                        success:function(res) {
                                        }
                                    });
                                    count=0;
                                    }
                                window.localStorage.setItem('count',count);
                                alert("Redirecting to newly downloaded song: "+songname);
                                $('.play-song[data-id="'+id+'"]').trigger('click');
                            }
                        });
                    },function(error) {
                        alert("Download of "+songname+" failed: "+error.code);
                    });
            });
 
        });    
    });
    
}

document.addEventListener("deviceready", onAppReady, false);


