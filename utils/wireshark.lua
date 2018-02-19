-- Nano/RaiBlocks Protocol Wireshark Dissector
-- Usage: $ wireshark -X lua_script:wireshark.lua nano.cap


function open_dissector_280(buffer, subtree)
    subtree = subtree:add(buffer(8, 272), "Open Block")
    -- print(buffer(8, 16), buffer(24, 16))
    subtree:add(buffer(8,   32),  "Representative?: "               .. buffer(8,   32))
    subtree:add(buffer(40,  64),  "Representative Signature?: "     .. buffer(40,  64))
    subtree:add(buffer(104, 8 ),  "Unknown Magic Number?: "         .. buffer(104, 8 ))
    subtree:add(buffer(112, 32),  "Hash of Source Block: "          .. buffer(112, 32))
    subtree:add(buffer(144, 32),  "Representative Account: "        .. buffer(144, 32))
    subtree:add(buffer(176, 32),  "Open Account: "                  .. buffer(176, 32))
    subtree:add(buffer(208, 64),  "Signature: "                     .. buffer(208, 64))
    subtree:add(buffer(272, 8 ),  "Work: "                          .. buffer(272, 8 ))
end


function send_dissector_264(buffer, subtree)
    subtree = subtree:add(buffer(8, 256), "Send Block")
    -- print(buffer(8, 16), buffer(24, 16))
    subtree:add(buffer(8,   32),  "Representative?: "               .. buffer(8,   32))
    subtree:add(buffer(40,  64),  "Representative Signature?: "     .. buffer(40,  64))
    subtree:add(buffer(104, 8 ),  "Unknown Magic Number?: "         .. buffer(104, 8 ))
    subtree:add(buffer(112, 32),  "Hash of Previous Block: "        .. buffer(112, 32))
    subtree:add(buffer(144, 32),  "Destination Account: "           .. buffer(144, 32))
    subtree:add(buffer(176, 16),  "Balance: "                       .. buffer(176, 16))
    subtree:add(buffer(192, 64),  "Signature: "                     .. buffer(192, 64))
    subtree:add(buffer(256, 8 ),  "Work: "                          .. buffer(256, 8 ))
end


function receive_dissector_248(buffer, subtree)
    subtree = subtree:add(buffer(8, 240), "Receive Block")
    -- print(buffer(8, 16), buffer(24, 16))
    subtree:add(buffer(8,   32),  "Representative?: "               .. buffer(8,   32))
    subtree:add(buffer(40,  64),  "Representative Signature?: "     .. buffer(40,  64))
    subtree:add(buffer(104, 8 ),  "Unknown Magic Number?: "         .. buffer(104, 8 ))
    subtree:add(buffer(112, 32),  "Hash of Previous Block: "        .. buffer(112, 32))
    subtree:add(buffer(144, 32),  "Hash of Source Block: "          .. buffer(144, 32))
    subtree:add(buffer(176, 64),  "Signature: "                     .. buffer(176, 64))
    subtree:add(buffer(240, 8 ),  "Work: "                          .. buffer(240, 8 ))
end


function open_dissector_176(buffer, subtree)
    subtree = subtree:add(buffer(8, 168), "Open Block")
    subtree:add(buffer(8,   32),  "Hash of Source Block: "      .. buffer(8,   32))
    subtree:add(buffer(40,  32),  "Representative Account: "    .. buffer(40,  32))
    subtree:add(buffer(72,  32),  "Open Account: "              .. buffer(72,  32))
    subtree:add(buffer(104, 64),  "Signature: "                 .. buffer(104, 64))
    subtree:add(buffer(168, 8 ),  "Work: "                      .. buffer(168, 8))
end


function send_dissector_160(buffer, subtree)
    subtree = subtree:add(buffer(8, 152), "Send Block")
    subtree:add(buffer(8,   32),  "Hash of Previous Block: "    .. buffer(8,   32))
    subtree:add(buffer(40,  32),  "Destination Account: "       .. buffer(40,  32))
    subtree:add(buffer(72,  16),  "Balance: "                   .. buffer(72,  16))
    subtree:add(buffer(88,  64),  "Signature: "                 .. buffer(88,  64))
    subtree:add(buffer(152, 8 ),  "Work: "                      .. buffer(152, 8 ))
end


function receive_dissector_144(buffer, subtree)
    subtree = subtree:add(buffer(8, 136), "Receive Block")
    subtree:add(buffer(8,   32),  "Hash of Previous Block: "    .. buffer(8,   32))
    subtree:add(buffer(40,  32),  "Hash of Source Block: "      .. buffer(40,  32))
    subtree:add(buffer(72,  64),  "Signature: "                 .. buffer(72,  64))
    subtree:add(buffer(136, 8 ),  "Work: "                      .. buffer(136, 8 ))
end


function peers_dissector_152(buffer, subtree)
    -- Port is in network byte order
    subtree = subtree:add(buffer(8, 144), "Peers")
    subtree:add(buffer(8,   16),  "IP: "        .. buffer(8,   16))
    subtree:add(buffer(24,   2),  "Port: "      .. buffer(24,   2))
    subtree:add(buffer(26,  16),  "IP: "        .. buffer(26,  16))
    subtree:add(buffer(42,   2),  "Port: "      .. buffer(42,   2))
    subtree:add(buffer(44,  16),  "IP: "        .. buffer(44,  16))
    subtree:add(buffer(60,   2),  "Port: "      .. buffer(60,   2))
    subtree:add(buffer(62,  16),  "IP: "        .. buffer(62,  16))
    subtree:add(buffer(78,   2),  "Port: "      .. buffer(78,   2))
    subtree:add(buffer(80,  16),  "IP: "        .. buffer(80,  16))
    subtree:add(buffer(96,   2),  "Port: "      .. buffer(96,   2))
    subtree:add(buffer(98,  16),  "IP: "        .. buffer(98,  16))
    subtree:add(buffer(114,  2),  "Port: "      .. buffer(114,  2))
    subtree:add(buffer(116, 16),  "IP: "        .. buffer(116, 16))
    subtree:add(buffer(132,  2),  "Port: "      .. buffer(132,  2))
    subtree:add(buffer(134, 16),  "IP: "        .. buffer(134, 16))
    subtree:add(buffer(150,  2),  "Port: "      .. buffer(150,  2))
end


nano_proto = Proto("nano", "Nano Protocol")

function nano_proto.dissector(buffer, pinfo, tree)
    pinfo.cols.protocol = "Nano"
    local subtree = tree:add(nano_proto, buffer(), "Nano Protocol")
    local txn_header = tostring(buffer(0, 8))
    local buf_len = buffer:len()
    -- print(txn_header, pinfo.src)
    -- rai/core_test/message.cpp (53n)
    -- rai/node/common.cpp (11n)
    header_tree = subtree:add(buffer(0, 8), "Header")
    header_tree:add(buffer(0, 2), "Stream?: "               .. buffer(0, 2))
    header_tree:add(buffer(2, 1), "Version Max: "       .. buffer(2, 1))
    header_tree:add(buffer(3, 1), "Version Using: "     .. buffer(3, 1))
    header_tree:add(buffer(4, 1), "Version Min: "       .. buffer(4, 1))
    header_tree:add(buffer(5, 1), "Message Type: "      .. buffer(5, 1))  -- rai/node/common.hpp (85n): enum class message_type : uint8_t
    header_tree:add(buffer(6, 1), "Extensions?: "       .. buffer(6, 1))
    header_tree:add(buffer(7, 1), "Block Type: "        .. buffer(7, 1))  -- rai/lib/blocks.hpp (32n): enum class block_type : uint8_t

    if buf_len == 280 then
        pinfo.cols.protocol = "Nano Open"
        open_dissector_280(buffer, subtree)
    elseif buf_len == 264 then
        pinfo.cols.protocol = "Nano Send"
        send_dissector_264(buffer, subtree)
    elseif buf_len == 248 then
        pinfo.cols.protocol = "Nano Receive"
        receive_dissector_248(buffer, subtree)
    elseif buf_len == 176 then
        pinfo.cols.protocol = "Nano Open"
        open_dissector_176(buffer, subtree)
    elseif buf_len == 160 then
        pinfo.cols.protocol = "Nano Send"
        send_dissector_160(buffer, subtree)
    elseif buf_len == 144 then
        pinfo.cols.protocol = "Nano Receive"
        receive_dissector_144(buffer, subtree)
    elseif buf_len == 152 then
        pinfo.cols.protocol = "Nano Keepalive"
        peers_dissector_152(buffer, subtree)
    end
end


udp_table = DissectorTable.get("udp.port")

udp_table:add(7075, nano_proto)

