%s

<h3 class="subtitle">Picture upload form</h3>

<form action="" method="post" enctype="multipart/form-data">
    <p>Select the flower you want to analyze and upload it.</p>

    <div class="file">
        <label class="file-label">
            <input class="file-input" type="file" name="file">
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

    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link" onclick="window.pleaseWait();">Upload picture</button>
        </div>
        <div class="control">
            <button class="button is-link is-light" onclick="window.location.replace('/'); return false;">Cancel</button>
        </div>
    </div>
</form>
