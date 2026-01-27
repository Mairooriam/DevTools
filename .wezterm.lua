local wezterm = require("wezterm")

local config = wezterm.config_builder()

-- CHANGE DEFUALT CWD WHEN CLONE
local default_path = "C:/Users/35850/Desktop/repositories"

config.default_cwd = default_path

config.initial_cols = 120
config.initial_rows = 28

config.font_size = 10
config.color_scheme = "Vs Code Dark+ (Gogh)"
--config.color_scheme = "Dracula"
-- config.color_scheme = "Espresso"
config.default_prog = { "pwsh" }
config.enable_scroll_bar = true

-- KEYBINDINGS
config.keys = {
	-- COPY STUFF
	{ key = "c", mods = "CTRL|SHIFT", action = wezterm.action.CopyTo("Clipboard") },
	{ key = "v", mods = "CTRL|SHIFT", action = wezterm.action.PasteFrom("Clipboard") },

	-- TAB STUFF
	{ key = "1", mods = "CTRL", action = wezterm.action.ActivateTab(0) },
	{ key = "2", mods = "CTRL", action = wezterm.action.ActivateTab(1) },
	{ key = "3", mods = "CTRL", action = wezterm.action.ActivateTab(2) },
	{ key = "4", mods = "CTRL", action = wezterm.action.ActivateTab(3) },
	{ key = "5", mods = "CTRL", action = wezterm.action.ActivateTab(4) },
	{ key = "6", mods = "CTRL", action = wezterm.action.ActivateTab(5) },
	{ key = "7", mods = "CTRL", action = wezterm.action.ActivateTab(6) },
	{ key = "8", mods = "CTRL", action = wezterm.action.ActivateTab(7) },
	{ key = "9", mods = "CTRL", action = wezterm.action.ActivateTab(-1) },

	-- VIM STYLE STUFF
	{ key = "u", mods = "CTRL", action = wezterm.action.ScrollByPage(-0.75) },
	{ key = "d", mods = "CTRL", action = wezterm.action.ScrollByPage(0.75) },
}

wezterm.on("gui-startup", function(cmd)
	local mux = wezterm.mux
	local tab1, pane1, window = mux.spawn_window({
		cwd = default_path,
	})

	local tab2 = window:spawn_tab({
		cwd = default_path,
	})

	local tab3 = window:spawn_tab({
		cwd = default_path,
	})
end)

return config