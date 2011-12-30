$(function() {
    /* PLATFORM DETECTION */
    window.using_phonegap = (!_.isUndefined(window.device));
    var uagent = navigator.userAgent.toLowerCase();
    window.platform = null;
    
    if (uagent.search('android') > -1) {
        platform = 'android';
    } else if (uagent.search('ipad') > -1) {
        platform = 'ipad';
    } else if (uagent.search('ipod') > -1 || uagent.search('iphone') > -1) {
        platform = 'iphone';
    } else if (uagent.search('blackberry') > -1) {
        platform = 'blackberry';
    }

    /* PAGES */
    function showHome() {
        $(".page").hide()
        $("#home").show();

        $(window).scrollTop(0)
    }

    function showAbout() { 
        $(".page").hide()
        $("#about").show();

        $(window).scrollTop(0)
    }

    /* URL ROUTING */
    window.CitizenRouter = Backbone.Router.extend({
        routes: {
            "":             "home",
            "about":        "about"
        },

        home: function() {
            showHome();
        },

        about: function() {
            showAbout();
        }
    });

    window.Router = new CitizenRouter();

    /* EVENT HANDLERS */
    $('header h1').click(function() {
        window.location.hash = "";
    });

    $("#view-about").click(function() {
        window.location.hash = "about";
    });

    $(".close").click(function() {
        history.back(); 
    });

    Backbone.history.start();
});

