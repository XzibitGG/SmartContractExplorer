from web3 import Web3

def parse_to_arg(arg, arg_type):
    if arg_type == 'bool':
        return arg.lower() in ("yes", "true", "t", "1")
    elif "uint" in arg_type:
        if "0x" in arg:
            return abs(Web3.toInt(hexstr = arg))
        else:
            return abs(Web3.toInt(text = arg))
    elif "int" in arg_type:
        if "0x" in arg:
            return Web3.toInt(hexstr = arg)
        else:
            return Web3.toInt(text = arg)
    elif "bytes" in arg_type:
        return Web3.toBytes(arg)
    elif "address" in arg_type:
        return Web3.toChecksumAddress(arg)
    return Web3.toJSON(arg)