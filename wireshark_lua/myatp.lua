do
    local p_atp = Proto("MYATP","Advanced Technology Protocol")

    local f = p_atp.fields
    f.bitmap = ProtoField.uint32("atp.bitmap", "Bitmap", base.HEX)
    f.agtr_time = ProtoField.uint8("atp.agtr_time", "Agtr Time", base.HEX)
    f.overflow = ProtoField.uint8("atp.overflow", "Overflow", base.HEX)
    f.PSIndex = ProtoField.uint8("atp.PSIndex", "PS Index", base.HEX)
    f.dataIndex = ProtoField.uint8("atp.dataIndex", "Data Index", base.HEX)
    f.ECN = ProtoField.uint8("atp.ECN", "ECN", base.HEX)
    f.isResend = ProtoField.uint8("atp.isResend", "Is Resend", base.HEX)
    f.isSWCollision = ProtoField.uint8("atp.isSWCollision", "Is SW Collision", base.HEX)
    f.isACK = ProtoField.uint8("atp.isACK", "Is ACK", base.HEX)
    f.appIDandSeqNum = ProtoField.uint32("atp.appIDandSeqNum", "App ID and Seq Num", base.HEX)
    f.p4ml_agtr_index = ProtoField.uint16("atp.p4ml_agtr_index", "P4ML Agtr Index", base.HEX)
    
    for i = 0, 31 do
        f["data" .. i] = ProtoField.uint32("atp.data" .. i, "Data " .. i, base.HEX)
    end

    local data_dis = Dissector.get("data")

    local function DT_dissector(buffer, pinfo, tree)

        local buf_len = buffer:len();
        if buf_len < 140 then return false end

        pinfo.cols.protocol = "ATP"
        local subtree = tree:add(p_atp, buffer(), "Advanced Technology Protocol Data")
        subtree:add(f.bitmap, buffer(0,4))
        subtree:add(f.agtr_time, buffer(4,1))
        -- subtree:add(f.option, buffer(5,1))
        local opt = buffer(5,1):uint()
        local myField = bit.band(bit.rshift(opt, 7), 0x01)
        subtree:add(f.overflow, myField)
        myField = bit.band(bit.rshift(opt, 5), 0x03)
        subtree:add(f.PSIndex, myField)
        myField = bit.band(bit.rshift(opt, 4), 0x01)
        subtree:add(f.dataIndex, myField)
        myField = bit.band(bit.rshift(opt, 3), 0x01)
        subtree:add(f.ECN, myField)
        myField = bit.band(bit.rshift(opt, 2), 0x01)
        subtree:add(f.isResend, buffer(9,1))
        myField = bit.band(bit.rshift(opt, 1), 0x01)
        subtree:add(f.isSWCollision, myField)
        myField = bit.band(bit.rshift(opt, 0), 0x01)
        subtree:add(f.isACK, myField)
        subtree:add(f.appIDandSeqNum, buffer(6,4))
        subtree:add(f.p4ml_agtr_index, buffer(10,2))

        for i = 0, 31 do
            subtree:add(f["data" .. i], buffer(12 + i * 4, 4))
        end
        return true
    end

    function p_atp.dissector(buffer, pinfo, tree)
        if not DT_dissector(buffer, pinfo, tree) then
            data_dis:call(buffer, pinfo, tree)
        end
    end

    local udp_dstport = DissectorTable.get("udp.port")
    udp_dstport:add(6001, p_atp)
end