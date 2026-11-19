function dumpglyphs(label)
 local out={}; local function walk(head)
  for n in node.traverse(head) do
   if n.id==node.id('glyph') then out[#out+1]=string.format('U+%04X',n.char)
   elseif n.id==node.id('hlist') or n.id==node.id('vlist') then walk(n.head) end
  end
 end
 walk(tex.box[0].head);texio.write_nl('FGA-MATH-'..label..': '..table.concat(out,' '))
end
