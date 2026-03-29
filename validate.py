
import sys
import os
import importlib
from pathlib import Path

def print_header(msg: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")

def print_check(passed: bool, msg: str):
    """Print a check result."""
    symbol = "✓" if passed else "✗"
    status = "PASS" if passed else "FAIL"
    print(f"  [{symbol}] {msg:<50} [{status}]")

def check_python_version():
    """Check Python version."""
    print_header("1. Python Version")
    
    version = sys.version_info
    min_version = (3, 6)
    passed = version >= min_version
    
    print(f"  Current: Python {version.major}.{version.minor}.{version.micro}")
    print(f"  Required: Python {min_version[0]}.{min_version[1]}+")
    print_check(passed, "Python version compatible")
    
    return passed

def check_dependencies():
    """Check required dependencies."""
    print_header("2. Dependencies")
    
    dependencies = {
        "requests": "HTTP requests library",
    }
    
    all_passed = True
    for package, description in dependencies.items():
        try:
            importlib.import_module(package)
            print_check(True, f"{package:<20} {description}")
        except ImportError:
            print_check(False, f"{package:<20} {description}")
            all_passed = False
    
    if not all_passed:
        print("\n  Install missing dependencies:")
        print("    pip install -r requirements.txt")
    
    return all_passed

def check_project_structure():
    """Check project structure."""
    print_header("3. Project Structure")
    
    base_path = Path(__file__).parent
    required_files = [
        ("bot/__init__.py", "Package init"),
        ("bot/client.py", "API client"),
        ("bot/orders.py", "Order logic"),
        ("bot/validators.py", "Input validation"),
        ("bot/logging_config.py", "Logging config"),
        ("cli.py", "CLI interface"),
        ("requirements.txt", "Dependencies"),
        ("README.md", "Documentation"),
    ]
    
    all_passed = True
    for file_path, description in required_files:
        full_path = base_path / file_path
        exists = full_path.exists()
        print_check(exists, f"{file_path:<30} {description}")
        if not exists:
            all_passed = False
    
    return all_passed

def check_api_modules():
    """Check that API modules can be imported."""
    print_header("4. Module Imports")
    
    modules = {
        "bot.client": "BinanceFuturesClient",
        "bot.orders": "place_order",
        "bot.validators": "validate_symbol",
        "bot.logging_config": "api_logger",
    }
    
    all_passed = True
    for module_name, item in modules.items():
        try:
            module = importlib.import_module(module_name)
            has_item = hasattr(module, item)
            print_check(has_item, f"from {module_name} import {item}")
            if not has_item:
                all_passed = False
        except Exception as e:
            print_check(False, f"Import {module_name}: {str(e)[:40]}")
            all_passed = False
    
    return all_passed

def check_api_credentials():
    """Check API credentials are configured."""
    print_header("5. API Credentials")
    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    has_key = bool(api_key)
    has_secret = bool(api_secret)
    
    print_check(has_key, "BINANCE_API_KEY environment variable set")
    print_check(has_secret, "BINANCE_API_SECRET environment variable set")
    
    if has_key:
        # Show first and last 6 chars for verification
        masked_key = f"{api_key[:6]}...{api_key[-6:]}"
        print(f"      Key (masked): {masked_key}")
    
    if has_secret:
        masked_secret = f"{api_secret[:6]}...{api_secret[-6:]}"
        print(f"      Secret (masked): {masked_secret}")
    
    if not (has_key and has_secret):
        print("\n  Set credentials:")
        print("    Windows (PowerShell):")
        print('      $env:BINANCE_API_KEY = "your_key"')
        print('      $env:BINANCE_API_SECRET = "your_secret"')
        print("    Mac/Linux:")
        print('      export BINANCE_API_KEY="your_key"')
        print('      export BINANCE_API_SECRET="your_secret"')
    
    return has_key and has_secret

def check_api_connectivity():
    """Check connectivity to Binance API (optional)."""
    print_header("6. API Connectivity (Optional)")
    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not (api_key and api_secret):
        print_check(False, "Credentials not set (skipping API test)")
        return None
    
    try:
        from bot.client import BinanceFuturesClient
        client = BinanceFuturesClient(api_key, api_secret, timeout=5)
        
        # Try to get exchange info (no signature needed)
        info = client.get_exchange_info()
        if info and "symbols" in info:
            num_symbols = len(info["symbols"])
            print_check(True, f"Connected to Binance API ({num_symbols} symbols)")
            return True
        else:
            print_check(False, "Invalid response from API")
            return False
            
    except Exception as e:
        error_msg = str(e)[:50]
        print_check(False, f"API connection: {error_msg}")
        return False

def check_input_validation():
    """Check input validators work."""
    print_header("7. Input Validation")
    
    try:
        from bot.validators import (
            validate_symbol,
            validate_side, 
            validate_order_type,
            validate_quantity,
            validate_price,
            ValidationError
        )
        
        test_cases = [
            (validate_symbol, "btcusdt", "Symbol validation"),
            (validate_side, "buy", "Side validation"),
            (validate_order_type, "market", "Order type validation"),
            (validate_quantity, "1.5", "Quantity validation"),
            (validate_price, "45000", "Price validation"),
        ]
        
        all_passed = True
        for validator, test_input, description in test_cases:
            try:
                result = validator(test_input)
                print_check(True, description)
            except ValidationError as e:
                print_check(False, f"{description}: {str(e)[:30]}")
                all_passed = False
        
        # Test invalid input
        try:
            validate_symbol("X")  # Too short
            print_check(False, "Invalid input rejection")
            return False
        except ValidationError:
            print_check(True, "Invalid input rejection")
        
        return all_passed
        
    except Exception as e:
        print_check(False, f"Error: {str(e)[:40]}")
        return False

def check_logs_directory():
    """Check logs directory is ready."""
    print_header("8. Logs Directory")
    
    logs_dir = Path(__file__).parent / "logs"
    
    if logs_dir.exists() and logs_dir.is_dir():
        print_check(True, "logs/ directory exists")
        
        log_files = list(logs_dir.glob("*.log"))
        print(f"      Found {len(log_files)} log files")
        for log_file in log_files:
            print(f"        - {log_file.name}")
        
        return True
    else:
        print_check(False, "logs/ directory not found")
        print("\n  Bot will create logs/ on first run")
        return True  # Not critical

def main():
    """Run all checks."""
    print("\n" + "="*60)
    print("  BINANCE TRADING BOT - SETUP VALIDATION")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Module Imports", check_api_modules),
        ("API Credentials", check_api_credentials),
        ("API Connectivity", check_api_connectivity),
        ("Input Validation", check_input_validation),
        ("Logs Directory", check_logs_directory),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            result = check_func()
            results[name] = result
        except Exception as e:
            print(f"\n  ERROR: {str(e)}")
            results[name] = False
    
    # Summary
    print_header("SUMMARY")
    
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    print(f"  Passed:  {passed}")
    print(f"  Failed:  {failed}")
    print(f"  Skipped: {skipped}")
    
    # Recommendations
    if results["API Credentials"]:
        if results["API Connectivity"] is not False:  # Can be None (skipped)
            print("\n✓ Bot is ready! Run:")
            print("  python cli.py -s BTCUSDT -S BUY -t MARKET -q 0.001")
        else:
            print("\n⚠ API connectivity check failed. Check:")
            print("  - Credentials are correct")
            print("  - Internet connection is working")
            print("  - Testnet API is accessible")
    else:
        print("\n⚠ API credentials not set. Set environment variables:")
        print("  export BINANCE_API_KEY='your_key'")
        print("  export BINANCE_API_SECRET='your_secret'")
    
    if results["Dependencies"] is False:
        print("\n  Install dependencies: pip install -r requirements.txt")
    
    if results["Project Structure"] is False:
        print("\n  Project structure issue - ensure all files exist")
    
    print("\n" + "="*60 + "\n")
    
    # Exit code
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
