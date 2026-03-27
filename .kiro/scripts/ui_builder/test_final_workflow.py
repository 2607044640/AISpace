"""
Final Validation Test for tscn-editor-tools

This comprehensive test validates the complete workflow:
1. Load SettingsMenuV2.tscn using TscnEditor
2. Make modifications (color, text, add node, remove node)
3. Save to test output file
4. Reload using TscnReader
5. Verify all modifications applied correctly
6. Verify UIDs, references, formatting preserved
7. Test that Godot can parse the file
"""

import sys
from pathlib import Path

# Add tscn_editor_tools to path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools.editor import TscnEditor
from tscn_editor_tools.reader import TscnReader
from tscn_editor_tools.types import Color, ParseError, EditorError


class TestResult:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, test_name):
        """Assert equality and track result"""
        if actual == expected:
            self.passed += 1
            print(f"✓ {test_name}")
            return True
        else:
            self.failed += 1
            error_msg = f"✗ {test_name}\n  Expected: {expected}\n  Actual: {actual}"
            print(error_msg)
            self.errors.append(error_msg)
            return False
    
    def assert_true(self, condition, test_name):
        """Assert condition is true"""
        if condition:
            self.passed += 1
            print(f"✓ {test_name}")
            return True
        else:
            self.failed += 1
            error_msg = f"✗ {test_name}"
            print(error_msg)
            self.errors.append(error_msg)
            return False
    
    def assert_not_none(self, value, test_name):
        """Assert value is not None"""
        return self.assert_true(value is not None, test_name)
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        print("\n" + "="*60)
        print(f"TEST SUMMARY: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for error in self.errors:
                print(f"  {error}")
        print("="*60)
        return self.failed == 0


def main():
    """Run comprehensive workflow test"""
    
    print("="*60)
    print("TSCN EDITOR TOOLS - FINAL VALIDATION TEST")
    print("="*60)
    
    result = TestResult()
    
    # Paths
    input_file = Path("../3d-practice/A1UIScenes/SettingsMenuV2.tscn")
    output_file = Path("test_output.tscn")
    
    print(f"\nInput file: {input_file}")
    print(f"Output file: {output_file}")
    
    # ===== STEP 1: Load file with TscnEditor =====
    print("\n" + "-"*60)
    print("STEP 1: Load SettingsMenuV2.tscn")
    print("-"*60)
    
    try:
        editor = TscnEditor(str(input_file))
        print("✓ File loaded successfully")
        
        # Verify initial state
        initial_node_count = len(editor._tree.nodes)
        print(f"  Initial node count: {initial_node_count}")
        
        result.assert_true(initial_node_count > 0, "Initial tree has nodes")
        
    except Exception as e:
        print(f"✗ Failed to load file: {e}")
        return False
    
    # ===== STEP 2: Make modifications =====
    print("\n" + "-"*60)
    print("STEP 2: Make modifications")
    print("-"*60)
    
    # 2.1: Update Background color
    print("\n2.1: Update Background_ColorRect color property")
    try:
        new_color = Color(0.2, 0.3, 0.4, 1.0)
        editor.update_property("Background_ColorRect", "color", new_color)
        print(f"  ✓ Updated color to {new_color}")
        result.passed += 1
    except Exception as e:
        print(f"  ✗ Failed to update color: {e}")
        result.failed += 1
        result.errors.append(f"Update color failed: {e}")
    
    # 2.2: Update button text properties
    print("\n2.2: Update button text properties")
    try:
        editor.update_property(
            "MainMargin_MarginContainer/MainVBox_VBoxContainer/ButtonsMargin_MarginContainer/Buttons_HBoxContainer/BackButton_Button",
            "text",
            "Go Back"
        )
        print("  ✓ Updated BackButton text to 'Go Back'")
        result.passed += 1
        
        editor.update_property(
            "MainMargin_MarginContainer/MainVBox_VBoxContainer/ButtonsMargin_MarginContainer/Buttons_HBoxContainer/ResetButton_Button",
            "text",
            "Reset All"
        )
        print("  ✓ Updated ResetButton text to 'Reset All'")
        result.passed += 1
        
    except Exception as e:
        print(f"  ✗ Failed to update button text: {e}")
        result.failed += 1
        result.errors.append(f"Update button text failed: {e}")
    
    # 2.3: Add a new Label node
    print("\n2.3: Add new Label node")
    try:
        new_label = editor.add_node(
            name="TestLabel_Label",
            node_type="Label",
            parent_path="MainMargin_MarginContainer/MainVBox_VBoxContainer/Tabs_TabContainer/Controls/ControlsMargin_MarginContainer/ControlsContent_VBoxContainer",
            properties={
                "layout_mode": 2,
                "text": "This is a test label added by the editor",
                "horizontal_alignment": 1
            }
        )
        print(f"  ✓ Added new Label with unique_id: {new_label.unique_id}")
        result.passed += 1
        
    except Exception as e:
        print(f"  ✗ Failed to add Label: {e}")
        result.failed += 1
        result.errors.append(f"Add Label failed: {e}")
    
    # 2.4: Remove a safe node (Placeholder_Label)
    print("\n2.4: Remove Placeholder_Label node")
    try:
        node_to_remove = "MainMargin_MarginContainer/MainVBox_VBoxContainer/Tabs_TabContainer/Controls/ControlsMargin_MarginContainer/ControlsContent_VBoxContainer/Placeholder_Label"
        editor.remove_node(node_to_remove)
        print("  ✓ Removed Placeholder_Label")
        result.passed += 1
        
    except Exception as e:
        print(f"  ✗ Failed to remove node: {e}")
        result.failed += 1
        result.errors.append(f"Remove node failed: {e}")
    
    # ===== STEP 3: Save to test output file =====
    print("\n" + "-"*60)
    print("STEP 3: Save modifications")
    print("-"*60)
    
    try:
        editor.save(str(output_file))
        print(f"✓ Saved to {output_file}")
        result.passed += 1
        
        # Verify file exists
        result.assert_true(output_file.exists(), "Output file exists")
        
        # Check file size
        file_size = output_file.stat().st_size
        print(f"  Output file size: {file_size} bytes")
        result.assert_true(file_size > 0, "Output file is not empty")
        
    except Exception as e:
        print(f"✗ Failed to save file: {e}")
        result.failed += 1
        result.errors.append(f"Save failed: {e}")
        return False
    
    # ===== STEP 4: Reload using TscnReader =====
    print("\n" + "-"*60)
    print("STEP 4: Reload with TscnReader")
    print("-"*60)
    
    try:
        reader = TscnReader(str(output_file))
        print("✓ File reloaded successfully")
        result.passed += 1
        
        reloaded_node_count = len(reader.tree.nodes)
        print(f"  Reloaded node count: {reloaded_node_count}")
        
        # Node count should be: initial - 1 (removed) + 1 (added) = initial
        expected_count = initial_node_count
        result.assert_equal(
            reloaded_node_count,
            expected_count,
            f"Node count matches (expected {expected_count})"
        )
        
    except Exception as e:
        print(f"✗ Failed to reload file: {e}")
        result.failed += 1
        result.errors.append(f"Reload failed: {e}")
        return False
    
    # ===== STEP 5: Verify modifications =====
    print("\n" + "-"*60)
    print("STEP 5: Verify modifications")
    print("-"*60)
    
    # 5.1: Verify Background color
    print("\n5.1: Verify Background color")
    bg_node = reader.tree.get_node_by_path("Background_ColorRect")
    if result.assert_not_none(bg_node, "Background_ColorRect exists"):
        color_value = bg_node.properties.get("color")
        expected_color = Color(0.2, 0.3, 0.4, 1.0)
        result.assert_equal(color_value, expected_color, "Background color updated correctly")
    
    # 5.2: Verify button text
    print("\n5.2: Verify button text")
    back_button = reader.tree.get_node_by_path(
        "MainMargin_MarginContainer/MainVBox_VBoxContainer/ButtonsMargin_MarginContainer/Buttons_HBoxContainer/BackButton_Button"
    )
    if result.assert_not_none(back_button, "BackButton exists"):
        text_value = back_button.properties.get("text")
        result.assert_equal(text_value, "Go Back", "BackButton text updated correctly")
    
    reset_button = reader.tree.get_node_by_path(
        "MainMargin_MarginContainer/MainVBox_VBoxContainer/ButtonsMargin_MarginContainer/Buttons_HBoxContainer/ResetButton_Button"
    )
    if result.assert_not_none(reset_button, "ResetButton exists"):
        text_value = reset_button.properties.get("text")
        result.assert_equal(text_value, "Reset All", "ResetButton text updated correctly")
    
    # 5.3: Verify new Label exists
    print("\n5.3: Verify new Label")
    test_label = reader.tree.get_node_by_path(
        "MainMargin_MarginContainer/MainVBox_VBoxContainer/Tabs_TabContainer/Controls/ControlsMargin_MarginContainer/ControlsContent_VBoxContainer/TestLabel_Label"
    )
    if result.assert_not_none(test_label, "TestLabel_Label exists"):
        result.assert_equal(test_label.node_type, "Label", "New node has correct type")
        text_value = test_label.properties.get("text")
        result.assert_equal(
            text_value,
            "This is a test label added by the editor",
            "New Label has correct text"
        )
    
    # 5.4: Verify Placeholder_Label removed
    print("\n5.4: Verify Placeholder_Label removed")
    placeholder = reader.tree.get_node_by_path(
        "MainMargin_MarginContainer/MainVBox_VBoxContainer/Tabs_TabContainer/Controls/ControlsMargin_MarginContainer/ControlsContent_VBoxContainer/Placeholder_Label"
    )
    result.assert_true(placeholder is None, "Placeholder_Label removed successfully")
    
    # ===== STEP 6: Verify UIDs and references =====
    print("\n" + "-"*60)
    print("STEP 6: Verify UIDs and references")
    print("-"*60)
    
    # 6.1: Check all unique_ids are unique
    print("\n6.1: Verify unique_id uniqueness")
    unique_ids = [node.unique_id for node in reader.tree.nodes]
    unique_id_set = set(unique_ids)
    result.assert_equal(
        len(unique_ids),
        len(unique_id_set),
        "All unique_ids are unique"
    )
    
    # 6.2: Verify scene UID preserved
    print("\n6.2: Verify scene UID")
    result.assert_equal(
        reader.tree.header.scene_uid,
        "uid://bs256ppml668y",
        "Scene UID preserved"
    )
    
    # 6.3: Verify ext_resources preserved
    print("\n6.3: Verify ext_resources")
    ext_resource_count = len(reader.tree.ext_resources)
    print(f"  ExtResource count: {ext_resource_count}")
    result.assert_equal(ext_resource_count, 3, "All ext_resources preserved")
    
    # 6.4: Verify ext_resource UIDs
    print("\n6.4: Verify ext_resource UIDs")
    expected_uids = {
        "uid://dbaix0lcy10v2",
        "uid://dpf5ovda3xlpv",
        "uid://0st2knyluaer"
    }
    actual_uids = {res.uid for res in reader.tree.ext_resources}
    result.assert_equal(actual_uids, expected_uids, "ExtResource UIDs preserved")
    
    # ===== STEP 7: Validate .tscn syntax =====
    print("\n" + "-"*60)
    print("STEP 7: Validate .tscn syntax")
    print("-"*60)
    
    # 7.1: Check file starts with [gd_scene]
    print("\n7.1: Verify file format")
    content = output_file.read_text(encoding='utf-8')
    result.assert_true(
        content.startswith("[gd_scene"),
        "File starts with [gd_scene] header"
    )
    
    # 7.2: Check for required sections
    print("\n7.2: Verify required sections")
    result.assert_true("[ext_resource" in content, "File contains [ext_resource] sections")
    result.assert_true("[node" in content, "File contains [node] sections")
    
    # 7.3: Verify no syntax errors (try parsing again)
    print("\n7.3: Verify parseable")
    try:
        test_reader = TscnReader(str(output_file))
        print("  ✓ File can be parsed without errors")
        result.passed += 1
    except ParseError as e:
        print(f"  ✗ Parse error: {e}")
        result.failed += 1
        result.errors.append(f"Parse validation failed: {e}")
    
    # 7.4: Check Color formatting
    print("\n7.4: Verify Color formatting")
    result.assert_true(
        "Color(0.2, 0.3, 0.4, 1.0)" in content or "Color(0.2, 0.3, 0.4, 1)" in content,
        "Color values formatted correctly"
    )
    
    # 7.5: Check string formatting
    print("\n7.5: Verify string formatting")
    result.assert_true(
        'text = "Go Back"' in content,
        "String values formatted with quotes"
    )
    
    # ===== Print final summary =====
    success = result.print_summary()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! The tscn-editor-tools library is working correctly.")
        print(f"\nTest output saved to: {output_file}")
        print("You can open this file in Godot to verify it loads correctly.")
    else:
        print("\n⚠️  SOME TESTS FAILED. Please review the errors above.")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
