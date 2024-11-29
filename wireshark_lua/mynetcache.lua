do
    -- 
    -- 
    local p_netcache = Proto("MYNETCACHE","netcache")

    local f = p_netcache.fields
    f.op = ProtoField.uint8("netcache.op", "Op", base.HEX)
    f.seq = ProtoField.uint32("netcache.seq", "Seq", base.HEX)
    f.key = ProtoField.uint16("netcache.key", "Key", base.HEX)

    for i = 0, 15 do
        f["data" .. i] = ProtoField.uint32("netcache.data" .. i, "Data " .. i, base.HEX)
    end

    local data_dis = Dissector.get("data")

    local function DT_dissector(buffer, pinfo, tree)

        local buf_len = buffer:len();
        pinfo.cols.protocol = "NETCACHE"
        local subtree = tree:add(p_netcache, buffer(), "netcache")
        subtree:add(f.op, buffer(0,1))
        subtree:add(f.seq, buffer(1,4))
        -- subtree:add(f.option, buffer(5,1))
        subtree:add(f.key, buffer(5,2))
        for i = 0, 15 do
            subtree:add(f["data" .. i], buffer(7 + i * 4, 4))
        end
        return true
    end

    function p_netcache.dissector(buffer, pinfo, tree)
        if not DT_dissector(buffer, pinfo, tree) then
            data_dis:call(buffer, pinfo, tree)
        end
    end

    local udp_dstport = DissectorTable.get("udp.port")
    udp_dstport:add(50000, p_netcache)
end