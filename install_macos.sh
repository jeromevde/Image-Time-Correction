#!/bin/bash

# EXIF Datetime Updater - Installation Script for macOS
# This script helps set up the context menu service

echo "🖼️  EXIF Datetime Updater - macOS Setup"
echo "======================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This installer is for macOS only."
    exit 1
fi

# Check Python installation
echo "🐍 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Found: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Please install Python 3 first."
    echo "   You can download it from: https://www.python.org/downloads/"
    exit 1
fi

# Check and install required packages
echo "📦 Checking Python packages..."
MISSING_PACKAGES=()

python3 -c "import PIL" 2>/dev/null || MISSING_PACKAGES+=("Pillow")
python3 -c "import piexif" 2>/dev/null || MISSING_PACKAGES+=("piexif")
python3 -c "import tkinter" 2>/dev/null || MISSING_PACKAGES+=("tkinter")

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo "📥 Installing missing packages: ${MISSING_PACKAGES[*]}"
    
    # Install Pillow and piexif if needed
    if [[ " ${MISSING_PACKAGES[*]} " =~ " Pillow " ]] || [[ " ${MISSING_PACKAGES[*]} " =~ " piexif " ]]; then
        pip3 install Pillow piexif
        if [ $? -ne 0 ]; then
            echo "❌ Failed to install Python packages. Please run manually:"
            echo "   pip3 install Pillow piexif"
            exit 1
        fi
    fi
    
    # Check tkinter and suggest solution if missing
    if [[ " ${MISSING_PACKAGES[*]} " =~ " tkinter " ]]; then
        echo "⚠️  tkinter is missing. If you're using Homebrew Python, install it with:"
        echo "   brew install python-tk"
        echo ""
        echo "   Then run this installer again."
        exit 1
    fi
else
    echo "✅ All required packages are installed."
fi

# Make scripts executable
echo "🔧 Setting up file permissions..."
chmod +x "$(dirname "$0")/exif_datetime_service.sh"
chmod +x "$(dirname "$0")/exif_datetime_gui.py"

# Get the current directory
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Open Automator (press Cmd+Space, type 'Automator')"
echo "2. Create a new 'Quick Action'"
echo "3. Set 'Service receives' to 'files or folders' in 'Finder'"
echo "4. Add a 'Run Shell Script' action"
echo "5. Set 'Pass input' to 'as arguments'"
echo "6. Replace the script content with:"
echo ""
echo "#!/bin/bash"
echo "bash \"$CURRENT_DIR/exif_datetime_service.sh\" \"\$@\""
echo ""
echo "7. Save the service as 'Update EXIF Datetime'"
echo ""
echo "📖 For detailed instructions, see: MACOS_SETUP.md"
echo ""
echo "🎉 After setup, right-click on image files/folders in Finder!"

# Test the installation
echo ""
echo "🧪 Testing installation..."
python3 "$CURRENT_DIR/exif_datetime_gui.py" --help 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ GUI script is working correctly."
else
    echo "⚠️  There might be an issue with the GUI script."
fi

echo ""
echo "Done! 🎉"
