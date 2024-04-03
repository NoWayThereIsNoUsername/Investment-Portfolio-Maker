Cảm ơn bạn đã ghé thăm :D
- Mình viết script này với mục kết hợp các danh mục đầu tư bao gồm vàng, cổ phiếu và crypto vào cùng 1 chart. Script phù 
hợp với những người có nhu cầu theo dõi số liệu 3 khoản đầu tư trên trong cùng 1 biểu đồ, giúp tiết kiệm thời gian kiểm tra
và tính toán lời lỗ của từng hạng mục.
- Các thư viện cần tải thêm (bắt buộc): 
    + matplotlib
    + vnstock
    + numpy
    + beautifulsoup
    + pandas
- Mình sẽ upload cả 1 file excel mẫu để các bạn có thể tự thêm danh mục của mình
- LƯU Ý: Script chỉ hoạt động với thị trường vàng và cổ phiếu Việt Nam, bao gồm sàn HOSE, HNX và UPCOM.

* Một vài khuyết điểm:
    + Chỉ có thể tính toán giá vàng nhẫn HOẶC giá vàng miếng, không thể kết hợp cả 2
    + Giá cổ phiếu chỉ được update sau khi phiên giao dịch đã kết thúc (15h00)
    + Phải chỉnh directory thủ công khá nhiều :(

* MỘT SỐ LƯU Ý KHI DÙNG SCRIPT (QUAN TRỌNG):
  
  - Nếu bạn sở hữu vàng miếng, để giá trị trong ngoặc là 1, nếu là vàng nhẫn, vui lòng để 9 <img width="163" alt="image" src="https://github.com/NoWayThereIsNoUsername/Investment-Portfolio-Maker/assets/165937052/9a33246b-991f-45ae-b7d5-7b6047c72bbd">
  - ĐẶC BIỆT QUAN TRỌNG: File excel để lưu các thông tin liên quan đến các danh mục đầu tư BẮT BUỘC phải được lưu dưới định dạng .csv (comma delimited)
  - Vui lòng giữ nguyên các mã có sẵn trong file excel, và chuyển share (gold đối với vàng, crypto amount đối với crypto) về 0 nếu bạn không sở hữu chúng để
    code có thể hoạt động bình thường, chúng sẽ không hiện lên biểu đồ đâu nên đừng lo lắng.
  - Giá crypto vui lòng để ở tiền US Dollar

    Script được viết ra để phù hợp với nhu cầu bản thân nên các tính năng có thể không phù hợp với người khác. 
