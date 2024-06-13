-- creates a trigger that decreases
-- the quantity of an item after adding a new order
DROP TRIGGER IF EXISTS decrease_quan;
DELIMITER //
CREATE TRIGGER decrease_quan
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items 
    SET quantity = quantity - NEW.number 
    WHERE name = NEW.item_name;
END;
//
DELIMITER ;
