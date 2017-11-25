function onDeviceReady() {
    window.localStorage.clear();
    if(window.localStorage.getItem("information")==null)
        setInformation();
    if(window.localStorage.getItem("playlists")==null)
        setPlaylists();
    
};

function setInformation(){
    var user = prompt("Enter your name: ");
    var information = '{"user": "'+user+'", "playlists": "6", "512": {"songinfo": {"name": "song56"}, "playlists": [0, 1, 1, 0, 0, 0]}, "13": {"songinfo": {"name": "song11"}, "playlists": [0, 0, 1, 0, 1, 0]}, "19": {"songinfo": {"name": "song115"}, "playlists": [0, 0, 1, 1, 1, 0]}, "534": {"songinfo": {"name": "song58"}, "playlists": [1, 0, 0, 0, 0, 1]}, "536": {"songinfo": {"name": "song581"}, "playlists": [1, 0, 0, 0, 0, 0]}, "26": {"songinfo": {"name": "song121"}, "playlists": [0, 0, 1, 0, 0, 0]}, "29": {"songinfo": {"name": "song124"}, "playlists": [0, 0, 1, 0, 0, 0]}, "545": {"songinfo": {"name": "song59"}, "playlists": [1, 1, 0, 0, 0, 1]}, "37": {"songinfo": {"name": "song131"}, "playlists": [0, 1, 1, 0, 0, 0]}, "550": {"songinfo": {"name": "song6"}, "playlists": [1, 1, 0, 0, 0, 0]}, "39": {"songinfo": {"name": "song133"}, "playlists": [1, 0, 0, 0, 0, 1]}, "45": {"songinfo": {"name": "song139"}, "playlists": [0, 1, 1, 0, 0, 0]}, "47": {"songinfo": {"name": "song140"}, "playlists": [0, 1, 1, 0, 0, 0]}, "561": {"songinfo": {"name": "song7"}, "playlists": [0, 0, 0, 1, 1, 0]}, "562": {"songinfo": {"name": "song70"}, "playlists": [0, 0, 1, 0, 0, 0]}, "568": {"songinfo": {"name": "song76"}, "playlists": [0, 0, 1, 1, 0, 0]}, "58": {"songinfo": {"name": "song150"}, "playlists": [1, 1, 0, 0, 0, 0]}, "571": {"songinfo": {"name": "song79"}, "playlists": [1, 0, 0, 0, 0, 1]}, "574": {"songinfo": {"name": "song81"}, "playlists": [0, 0, 1, 0, 0, 0]}, "575": {"songinfo": {"name": "song82"}, "playlists": [0, 0, 1, 1, 0, 0]}, "577": {"songinfo": {"name": "song84"}, "playlists": [1, 1, 1, 0, 0, 0]}, "581": {"songinfo": {"name": "song88"}, "playlists": [1, 0, 0, 0, 0, 1]}, "583": {"songinfo": {"name": "song9"}, "playlists": [1, 1, 0, 0, 0, 0]}, "72": {"songinfo": {"name": "song163"}, "playlists": [0, 0, 0, 0, 0, 1]}, "585": {"songinfo": {"name": "song91"}, "playlists": [0, 0, 1, 1, 1, 0]}, "586": {"songinfo": {"name": "song92"}, "playlists": [0, 1, 1, 0, 0, 0]}, "525": {"songinfo": {"name": "song571"}, "playlists": [0, 1, 1, 0, 0, 0]}, "592": {"songinfo": {"name": "song98"}, "playlists": [0, 1, 0, 0, 0, 0]}, "93": {"songinfo": {"name": "song182"}, "playlists": [0, 1, 1, 0, 0, 0]}, "99": {"songinfo": {"name": "song188"}, "playlists": [1, 1, 0, 0, 0, 0]}, "116": {"songinfo": {"name": "song202"}, "playlists": [1, 1, 0, 0, 0, 1]}, "141": {"songinfo": {"name": "song225"}, "playlists": [0, 0, 0, 0, 0, 1]}, "538": {"songinfo": {"name": "song583"}, "playlists": [0, 0, 0, 0, 0, 1]}, "163": {"songinfo": {"name": "song245"}, "playlists": [0, 0, 1, 0, 0, 0]}, "164": {"songinfo": {"name": "song246"}, "playlists": [1, 0, 0, 0, 0, 1]}, "165": {"songinfo": {"name": "song247"}, "playlists": [0, 0, 0, 0, 0, 1]}, "166": {"songinfo": {"name": "song248"}, "playlists": [0, 0, 1, 0, 1, 0]}, "168": {"songinfo": {"name": "song25"}, "playlists": [0, 0, 1, 1, 1, 0]}, "178": {"songinfo": {"name": "song259"}, "playlists": [1, 0, 0, 0, 0, 0]}, "187": {"songinfo": {"name": "song267"}, "playlists": [0, 0, 1, 1, 0, 0]}, "195": {"songinfo": {"name": "song274"}, "playlists": [0, 1, 1, 0, 0, 0]}, "205": {"songinfo": {"name": "song283"}, "playlists": [0, 0, 0, 0, 0, 1]}, "208": {"songinfo": {"name": "song286"}, "playlists": [0, 0, 0, 0, 0, 1]}, "214": {"songinfo": {"name": "song291"}, "playlists": [1, 0, 0, 0, 0, 0]}, "221": {"songinfo": {"name": "song298"}, "playlists": [0, 0, 0, 0, 0, 1]}, "549": {"songinfo": {"name": "song593"}, "playlists": [0, 1, 1, 0, 0, 0]}, "230": {"songinfo": {"name": "song305"}, "playlists": [0, 0, 1, 1, 1, 0]}, "231": {"songinfo": {"name": "song306"}, "playlists": [1, 0, 0, 0, 0, 0]}, "233": {"songinfo": {"name": "song308"}, "playlists": [1, 1, 0, 0, 0, 0]}, "235": {"songinfo": {"name": "song31"}, "playlists": [0, 0, 1, 1, 1, 0]}, "236": {"songinfo": {"name": "song310"}, "playlists": [0, 1, 1, 0, 0, 0]}, "244": {"songinfo": {"name": "song318"}, "playlists": [0, 0, 1, 1, 0, 0]}, "252": {"songinfo": {"name": "song325"}, "playlists": [0, 0, 0, 1, 0, 0]}, "253": {"songinfo": {"name": "song326"}, "playlists": [0, 0, 1, 1, 1, 0]}, "254": {"songinfo": {"name": "song327"}, "playlists": [1, 1, 1, 0, 0, 0]}, "256": {"songinfo": {"name": "song329"}, "playlists": [0, 0, 1, 0, 1, 0]}, "257": {"songinfo": {"name": "song33"}, "playlists": [1, 0, 0, 0, 0, 1]}, "261": {"songinfo": {"name": "song333"}, "playlists": [0, 0, 0, 0, 0, 1]}, "263": {"songinfo": {"name": "song335"}, "playlists": [1, 1, 0, 0, 0, 0]}, "270": {"songinfo": {"name": "song341"}, "playlists": [0, 0, 0, 0, 1, 1]}, "278": {"songinfo": {"name": "song349"}, "playlists": [1, 0, 0, 0, 0, 1]}, "291": {"songinfo": {"name": "song360"}, "playlists": [0, 0, 1, 1, 1, 0]}, "295": {"songinfo": {"name": "song364"}, "playlists": [0, 0, 1, 1, 0, 1]}, "296": {"songinfo": {"name": "song365"}, "playlists": [1, 0, 0, 0, 0, 1]}, "300": {"songinfo": {"name": "song369"}, "playlists": [0, 0, 0, 1, 1, 0]}, "306": {"songinfo": {"name": "song374"}, "playlists": [1, 0, 0, 0, 1, 0]}, "312": {"songinfo": {"name": "song38"}, "playlists": [0, 0, 1, 0, 0, 0]}, "317": {"songinfo": {"name": "song384"}, "playlists": [0, 0, 1, 1, 0, 0]}, "322": {"songinfo": {"name": "song389"}, "playlists": [0, 0, 1, 0, 0, 0]}, "323": {"songinfo": {"name": "song39"}, "playlists": [0, 1, 1, 0, 0, 0]}, "326": {"songinfo": {"name": "song392"}, "playlists": [1, 1, 0, 0, 0, 0]}, "333": {"songinfo": {"name": "song399"}, "playlists": [0, 0, 1, 1, 1, 0]}, "339": {"songinfo": {"name": "song403"}, "playlists": [0, 0, 0, 0, 0, 1]}, "570": {"songinfo": {"name": "song78"}, "playlists": [0, 0, 1, 1, 1, 0]}, "361": {"songinfo": {"name": "song423"}, "playlists": [0, 0, 1, 1, 1, 0]}, "381": {"songinfo": {"name": "song441"}, "playlists": [0, 1, 1, 0, 0, 0]}, "382": {"songinfo": {"name": "song442"}, "playlists": [0, 1, 0, 0, 0, 0]}, "401": {"songinfo": {"name": "song46"}, "playlists": [0, 1, 1, 1, 0, 0]}, "402": {"songinfo": {"name": "song460"}, "playlists": [0, 0, 1, 1, 1, 0]}, "406": {"songinfo": {"name": "song464"}, "playlists": [0, 0, 1, 1, 1, 0]}, "409": {"songinfo": {"name": "song467"}, "playlists": [1, 1, 0, 0, 0, 0]}, "411": {"songinfo": {"name": "song469"}, "playlists": [1, 1, 0, 0, 0, 1]}, "416": {"songinfo": {"name": "song473"}, "playlists": [0, 0, 1, 1, 1, 0]}, "418": {"songinfo": {"name": "song475"}, "playlists": [0, 0, 0, 0, 0, 1]}, "423": {"songinfo": {"name": "song48"}, "playlists": [0, 0, 1, 0, 0, 0]}, "433": {"songinfo": {"name": "song489"}, "playlists": [0, 0, 1, 0, 1, 0]}, "438": {"songinfo": {"name": "song493"}, "playlists": [1, 0, 0, 0, 0, 1]}, "451": {"songinfo": {"name": "song504"}, "playlists": [0, 0, 1, 0, 0, 0]}, "456": {"songinfo": {"name": "song509"}, "playlists": [0, 0, 1, 0, 0, 0]}, "460": {"songinfo": {"name": "song512"}, "playlists": [0, 0, 1, 1, 1, 0]}, "466": {"songinfo": {"name": "song518"}, "playlists": [0, 1, 0, 0, 0, 1]}, "469": {"songinfo": {"name": "song520"}, "playlists": [0, 0, 1, 1, 0, 0]}, "473": {"songinfo": {"name": "song524"}, "playlists": [0, 0, 0, 0, 0, 1]}, "476": {"songinfo": {"name": "song527"}, "playlists": [0, 0, 0, 0, 1, 0]}, "487": {"songinfo": {"name": "song537"}, "playlists": [0, 0, 0, 0, 0, 1]}, "489": {"songinfo": {"name": "song539"}, "playlists": [0, 0, 0, 0, 1, 1]}, "497": {"songinfo": {"name": "song546"}, "playlists": [0, 0, 1, 1, 1, 0]}, "499": {"songinfo": {"name": "song548"}, "playlists": [0, 0, 1, 0, 0, 0]}, "509": {"songinfo": {"name": "song557"}, "playlists": [0, 0, 1, 1, 1, 0]}, "511": {"songinfo": {"name": "song559"}, "playlists": [0, 0, 0, 0, 0, 1]}}';
    
    window.localStorage.setItem("information",information);
    console.log(JSON.parse(window.localStorage.getItem('information')));
    information = JSON.parse(information);
    delete information.user;
    delete information.playlists;
    window.requestFileSystem(LocalFileSystem.PERSISTENT, 0, function (fs) {
        fs.root.getDirectory('songs',{create: true, exclusive: false}, function(dirEntry){
            var fileTransfer = new FileTransfer();
            $.each(information, function(id,song){
                var uri = encodeURI("http://192.168.43.249:5000/fetch?song="+song.songinfo['name']);
                var path = dirEntry.toURL();
                fileURL = path+song.songinfo['name']+".wav";
                var directoryEntry = path;
                fileTransfer.download(
                    uri,
                    fileURL
                );
            });
 
        },function(error){
            alert("2ERROR: "+error.code);
        });
        
        
    },function(error){
        alert("1ERROR: "+error.code);
    });
    
    $.ajax({
                url: 'http://192.168.43.249:5000/fit',
                type: 'GET',
                dataType: 'text',
                contentType: 'application/json; charset=utf-8',
                data: window.localStorage.getItem('information'),
                success:function(res) {
                }
            });
}



function setPlaylists(){
    console.log("storage");
    var playlists = '{"happy_pleased": ["37", "45", "47", "58", "93", "99", "116", "195", "233", "236", "254", "263", "323", "326", "381", "382", "401", "409", "411", "466", "512", "525", "545", "549", "550", "577", "583", "586", "592"], "amazed_surprised": ["39", "58", "99", "116", "164", "178", "214", "231", "233", "254", "257", "263", "278", "296", "306", "326", "409", "411", "438", "534", "536", "545", "550", "571", "577", "581", "583"], "quiet_still": ["19", "168", "187", "230", "235", "244", "252", "253", "291", "295", "300", "317", "333", "361", "401", "402", "406", "416", "460", "469", "497", "509", "561", "568", "570", "575", "585"], "relaxing_calm": ["13", "19", "26", "29", "37", "45", "47", "93", "163", "166", "168", "187", "195", "230", "235", "236", "244", "253", "254", "256", "291", "295", "312", "317", "322", "323", "333", "361", "381", "401", "402", "406", "416", "423", "433", "451", "456", "460", "469", "497", "499", "509", "512", "525", "549", "562", "568", "570", "574", "575", "577", "585", "586"], "angry_aggressive": ["39", "72", "116", "141", "164", "165", "205", "208", "221", "257", "261", "270", "278", "295", "296", "339", "411", "418", "438", "466", "473", "487", "489", "511", "534", "538", "545", "571", "581"], "sad_lonely": ["13", "19", "166", "168", "230", "235", "253", "256", "270", "291", "300", "306", "333", "361", "402", "406", "416", "433", "460", "476", "489", "497", "509", "561", "570", "585"]}';
    
    var mapping = {
        0: "amazed_surprised",
        1: "happy_pleased",
        2: "relaxing_calm",
        3: "quiet_still",
        4: "sad_lonely",
        5: "angry_aggressive"
    }
    
    window.localStorage.setItem("playlists",playlists);
    window.localStorage.setItem("mapping",JSON.stringify(mapping));
    window.localStorage.setItem("count",0);
    console.log(JSON.parse(window.localStorage.getItem('playlists')));
}

document.addEventListener("deviceready", onDeviceReady, false);