var chars = null

$(document).ready(function() {
    chars = $("#data").data("chars")

    // Char details feature is not implemented yet
    // setActiveChar(0)
});

function setActiveChar(index) {
    let allCharContainers = $("[id^=char-container-]")
    for (let i = 0; i < chars.length; i++) {
        $("#char-container-" + i).removeClass("char-container-active")
    }

    let charContainerId = "char-container-" + index.toString()
    $("#" + charContainerId).addClass("char-container-active")
}

function setCharInfo(map, job, level) {
    $("#td-lvl").text(level)
}