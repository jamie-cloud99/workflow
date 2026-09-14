on open documentsToPreview
    set readerScript to POSIX path of (path to resource "preview-markdown.sh")
    repeat with documentToPreview in documentsToPreview
        set documentPath to POSIX path of documentToPreview
        do shell script "/usr/bin/open -na Ghostty --args -e /bin/bash " & quoted form of readerScript & " " & quoted form of documentPath
    end repeat
end open

on run
    set chosenDocument to choose file with prompt "選擇要預覽的 Markdown 文件"
    open {chosenDocument}
end run
