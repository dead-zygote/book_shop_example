$(function(){
    $("body").on("submit", ".delete", function() {
        var message = $(this).data("message") || "Вы уверены?";
        return confirm(message);
    });
});
