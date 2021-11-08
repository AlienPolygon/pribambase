-- Copyright (c) 2021 lampysprites
-- 
-- Permission is hereby granted, free of charge, to any person obtaining a copy
-- of this software and associated documentation files (the "Software"), to deal
-- in the Software without restriction, including without limitation the rights
-- to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
-- copies of the Software, and to permit persons to whom the Software is
-- furnished to do so, subject to the following conditions:
-- 
-- The above copyright notice and this permission notice shall be included in all
-- copies or substantial portions of the Software.
-- 
-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
-- IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
-- FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
-- AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
-- LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
-- OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
-- SOFTWARE.

-- globals
pribambase_settings = nil -- refers to plugin.preferences
pribambase_default_settings = {
    host="localhost",
    port="34613",
    autostart=false,
    autoshow=false,
    maxsize="65535"
}


function run_script(f) 
    local s = app.fs.joinPath(app.fs.userConfigPath, "extensions", "pribambase", f) .. ".lua"

    return function()
        dofile(s)
    end
end


function init(plugin)
    -- fill the missing settings with default values
    for key,defval in pairs(pribambase_default_settings) do
        if type(plugin.preferences[key]) == "nil" then
            plugin.preferences[key] = defval
        end
    end

    -- expose settings
    pribambase_settings = plugin.preferences

    -- register new menus
    plugin:newCommand{
        id="SbSync",
        title="Sync",
        group="file_export",
        onclick=run_script("Sync")
    }

    plugin:newCommand{
        id="SbSyncSettings",
        title="Sync: Settings",
        onclick=run_script("Settings")
    }

    if plugin.preferences.autostart or plugin.preferences.autoshow then
        pribambase_start = true
        local ok, what = pcall(run_script("Sync"))
        if not ok then
            print("Could not start sync: " .. what)
        end
        pribambase_start = nil
    end
end