%(ERROR_MESSAGE)s

<h3 class="subtitle">Picture upload form</h3>

<p>Select the flower you want to analyze and upload it.</p>

<div class="container" id="info-uploading">
    <div class="notification is-info">
        <button class="delete" data-ignore-disabling onclick="this.parentElement.style.display = 'none';"></button>
        %(TEXT_UPLOAD)s
    </div>

    <p></p>
</div>

<div class="file">
    <label class="file-label">
        <input class="file-input" type="file" name="file" id="predict-file-source">
        <span class="file-cta">
            <span class="file-icon">
                <i class="fas fa-upload"></i>
            </span>
            <span class="file-label">
                Choose a file...
            </span>
        </span>
    </label>
</div>

<p>&nbsp;</p>

<form action="" method="post" enctype="multipart/form-data" id="prediction-form" onsubmit="return window.submitPicture();">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">Upload picture</button>
        </div>
        <div class="control">
            <button class="button is-link is-light" onclick="window.location.replace('/'); return false;">Cancel</button>
        </div>
    </div>

    <input type="hidden" name="predict-file-raw" value="" id="predict-file-raw">
    <input type="hidden" name="predict-file-name" value="" id="predict-file-name">
</form>
