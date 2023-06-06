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
        $("#recipe_name").text(data.recipe_name);
        $("#ingredients").text(data.ingredients);
        $("#comments").text(data.comments);
        $("#username").text(data.username);
        $("#recipe_name").attr(`data:image/jpeg;base64,${data.image}`);
        $("#search_button").text('Başka Tarif');
      },
      error: function (xhr, status, error) {
        console.log("Recipe Not Found!");
        jQuery.noConflict();
      },
    });
  });
});
