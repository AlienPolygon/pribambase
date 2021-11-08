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

local dlg = Dialog()


local function restoreDefaults()
    -- we must modify the fields, assigning an `{}` will overwrite
    -- the reference to the plugin settings, and they won't be affected
    for key,_ in pairs(pribambase_settings) do
        pribambase_settings[key] = nil
    end

    for key,_ in pairs(pribambase_default_settings) do
        pribambase_settings[key] = pribambase_default_settings[key]
    end
end


local function save()
    for key,_ in pairs(pribambase_default_settings) do
        pribambase_settings[key] = dlg.data[key]
    end
end


local function changeAutoshow()
    dlg:modify{ id="autoshow", visible=dlg.data.autostart }
end


dlg:separator{text="Connection"}
    :entry{id="host", label="Server", text=pribambase_settings.host}
    :entry{id="port", label="Port", text=pribambase_settings.port}
    :check{id="autostart", label="Connect when Aseprite launches", selected=pribambase_settings.autostart, onclick=changeAutoshow}
    :check{id="autoshow", label="Show when Aseprite launches", selected=pribambase_settings.autoshow, visible=dlg.data.autostart}
    :number{id="maxsize", label="Size Limit", decimals=0, text=tostring(pribambase_settings.maxsize)}

    :separator()
    :button{text="Defaults", onclick=restoreDefaults}
    :button{text="Cancel", focus=true}
    :button{text="OK", onclick=function() save() dlg:close() end}

    :show()