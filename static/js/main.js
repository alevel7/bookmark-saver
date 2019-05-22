$(function(){
    //mother function holds all code

    $('p').click(function(){
        alert("hello world");
    })

    $('form').hover(
        function(){
        $('form').css("background", "lightblue");
    },
        function(){
            $('form').css("background", "white");
    }
    )

    $('.btn').click(function(){
        $('form').show(1000)
    })
    $('.dropdown').click(function(){
        $('#sub').slideToggle(1000)
    })
})