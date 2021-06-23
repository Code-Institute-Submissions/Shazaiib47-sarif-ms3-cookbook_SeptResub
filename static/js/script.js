/* jshint esversion: 6 */

$(document).ready(function () {
    /* Side Nav */
    $('.sidenav').sidenav({
        edge: "right"
    });
    /* Accordion Collapsible with Form, Date Pickerr as well as the tooltip */
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: 'dd mmmm, yyyy',
        yearRange: 3,
        showClearBtn: true,
        il8n: {
            done: "Select"
        }
    });
    $('.modal').modal();

    /* Mobile Carousel Config */
    var mobileCarousel = $('.carousel-mobile.carousel.carousel-slider');
    mobileCarousel.carousel({
        // fullWidth: true,
        indicators: true,
        duration: 200,
    });

    var minstance = M.Carousel.getInstance(mobileCarousel);
    setInterval(function () {
        minstance.next();
    }, 3000);

    /* Desktop Carousel Configuration */
    var desktopCarousel = $('.carousel-desktop.carousel.carousel-slider');
    desktopCarousel.carousel({
        // fullWidth: true,
        indicators: true,
        duration: 200,
    });

    var dinstance = M.Carousel.getInstance(desktopCarousel);
    setInterval(function () {
        dinstance.next();
    }, 3000);


    /* Dropdown Validation */
    validateMaterializeSelect();

    function validateMaterializeSelect() {
        let classValid = {
            "border-bottom": "1px solid #4caf50",
            "box-shadow": "0 1px 0 0 #4caf50"
        };
        let classInvalid = {
            "border-bottom": "1px solid #f44336",
            "box-shadow": "0 1px 0 0 #f44336"
        };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({
                "display": "block",
                "height": "0",
                "padding": "0",
                "width": "0",
                "position": "absolute"
            });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () {})) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }
});