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
        const newSrc = `data:image/jpeg;base64,${data.image}`;
        $("#recipe_image").prop("src", newSrc);
        $("#search_button").text("Başka Tarif");
      },
      error: function (xhr, status, error) {
        $(".content").addClass("hidden");
        $(".alternative_content").removeClass("hidden");
        $(".alternative_content > p").remove();
        $(".alternative_content").append("<p>Tarif bulunamadı!<p>");
        $("#search_button").text("Başka Tarif");
        console.log("Recipe Not Found!");
        jQuery.noConflict();
      },
    });
  });
});
