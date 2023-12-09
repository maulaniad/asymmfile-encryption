
# Declare types to be used by models, this will act as an ENUM of allowed values.

ALLOWED_FILETYPES = (
    ('pdf', "Portable Document"),
    ('xls', "Excel Worksheet"),
    ('xlsx', "Excel Spreadsheet"),
    ('doc', "Word Document"),
    ('docx', "Word Text Document"),
    ('ppt', "Powerpoint Presentation"),
    ('pptx', "Powerpoint Presentation Document"),
    ('txt', "Plain Text"),
    ('md', "Markdown Documentation")
)

USER_ACTION = (
    ('encrypt', "File Encrypted"),
    ('decrypt', "File Decrypted"),
    ('delete', "File Deleted")
)
