<?php
/**
 * Plugin Name:       Random Plugin
 * Plugin URI:        https://example.com
 * Description:       A random plugin for testing purposes.
 * Version:           2.0.28
 * Author:            Random Author
 * Requires PHP:      7.4
 * Requires at least: 5.6
 * Tested up to:      5.9
 * Author URI:        https://example.com
 * License:           GPL-2.0+
 * License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
 * Text Domain:       random-plugin
 * Domain Path:       /languages
 *
 * @package RandomPlugin
 */

// Exit if accessed directly
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// Define plugin version
if ( ! defined( 'RANDOM_PLUGIN_VERSION' ) ) {
    define( 'RANDOM_PLUGIN_VERSION', '1.0.0' );
}

// Include necessary files
require_once plugin_dir_path( __FILE__ ) . 'includes/class-random-plugin.php';

// Initialize the plugin
function run_random_plugin() {
    $plugin = new Random_Plugin();
    $plugin->run();
}
run_random_plugin();
