$(document).ready(function () {
  $("#search_button").click(() => {
    console.log("Search button");
    const search_value = $("#search_value").val();

    $.ajax({
      type: "POST",
      contentType: "application/json",
      url: "/search",
      dataType: "json",
      data: JSON.stringify(search_value),
      success: (data) => {
        console.log(data);
        $(".content").addClass("hidden");
        $(".alternative_content").removeClass("hidden");
      },
      error: function (xhr, status, error) {
        console.log("Client Not Found!");
        jQuery.noConflict();
      },
    });
  });
});
