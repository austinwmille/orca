# Navigate to the script directory
Set-Location -Path $PSScriptRoot

# Activate the virtual environment
& .\cliaenv\Scripts\activate

# Run the Python script
python .\clipmev2.py

# Keep the session open for additional commands
Write-Host "Script finished! The virtual environment is still active. You can now enter more commands." -ForegroundColor Green
