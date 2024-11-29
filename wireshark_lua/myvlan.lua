do
    -- 
    -- 
    local p_zjvlan = Proto("MYVLAN","zjvlan")

    local f = p_zjvlan.fields
    f.vid = ProtoField.uint16("zjvlan.vid", "Vid", base.HEX)
    f.ethtype = ProtoField.uint16("zjvlan.ethtype", "Ethtype", base.HEX)

    local data_dis = Dissector.get("data")

    local function DT_dissector(buffer, pinfo, tree)
        local buf_len = buffer:len();
        pinfo.cols.protocol = "MYVLAN"
        local subtree = tree:add(p_zjvlan, buffer(), "zjvlan")
        subtree:add(f.vid, buffer(0,2))
        subtree:add(f.ethtype, buffer(2,2))
        return true
    end

    function p_zjvlan.dissector(buffer, pinfo, tree)
        if not DT_dissector(buffer, pinfo, tree) then
            data_dis:call(buffer, pinfo, tree)
        end
    end

    local eth = DissectorTable.get("ethertype")
    eth:add(0x0811, p_zjvlan)
end