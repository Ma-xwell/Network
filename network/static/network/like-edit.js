$(function () {

    $(document).on("click", ".edit-post-button", function() {
        var currentPost = $(this).closest(".flex-column-reverse");
        var currentContent = currentPost.find(".post-content")
        var originalContent = currentContent;
        var textarea = $('<textarea>').html(currentContent.html());
        currentContent.replaceWith(textarea);

        var editArea = $(this).closest(".edit-area").find('.edit-post-button');
        var originalEditArea = $(this).closest(".edit-area").html();
        var newButtons = $('<button class="save-post-button">SAVE</button><button class="cancel-post-button">Cancel</button>');
        editArea.replaceWith(newButtons);

        var saveButton = currentPost.find('.save-post-button');
        saveButton.click(function (){
            var postID = $(this).closest('.flex-column-reverse').find('.post-id').val();
            var newText = $(this).closest('.flex-column-reverse').find('textarea').val();
            $.ajax({
                url: `update-post/${postID}`,
                method: 'POST',
                data: newText,
                dataType: 'json'
            })
            .done(function() {
                $.ajax({
                    url: `get-new-post/${postID}`,
                    method: 'POST',
                    dataType: 'json'
                })
                .done(function(data) {
                    textarea.replaceWith($('<div class="p-1 post-content">').html(data.updatedText));
                    editArea = $(this).closest(".edit-area").html(originalEditArea);
                })
            })
            editArea = $(this).closest(".edit-area").html(originalEditArea);
        })

        var cancelButton = currentPost.find('.cancel-post-button');
        cancelButton.click(function (){
            textarea.replaceWith(originalContent);
            editArea = $(this).closest(".edit-area").html(originalEditArea);
        })
    })
})