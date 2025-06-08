# Custom lsp for python

Lsp for python k8s project that enables go to definiton from env to configmap.yaml. 
This file acutally defines env variables in k8s.

How to run in nvim 
```lua
function start_custom_lsp()
            local lsp = require('lsp-zero')
            vim.lsp.start({
                on_attach = lsp.on_attach,
                name = "custom-lsp",
                cmd = { "/build_path/PyLsp4/PyGoLspTest" },
                root_dir = vim.fn.getcwd(), -- Use PWD as project root dir.
            })
        end

vim.api.nvim_create_autocmd("FileType",
    {
        pattern = "python",
        callback = start_custom_lsp
    })

vim.api.nvim_create_autocmd("FileType",
    {
        pattern = "yaml",
        callback = start_custom_lsp
    })
```
